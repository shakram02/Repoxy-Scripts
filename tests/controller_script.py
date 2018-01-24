from __future__ import print_function
from entities.config_maker import ConfigMaker
from entities.controller_machine import ControllerMachineRx
from entities.networking.constants import DISCOVERY_PORT
from entities.networking.discovery_client import DiscoveryClient
from entities.networking.utils import get_ip


def test():
    """
    Phases:
    - Discovery: Clients keep broadcasting packets until the DiscoveryServer finds them
    the server then sends them a TCP port,

    The network machine will open a TCP server socket and wait for clients

    The network machine will run mininet ping test when all clients declare their controllers
    as ready
    """
    discovery_client = DiscoveryClient(DISCOVERY_PORT)
    machine_number = int(get_ip()[-1])
    config_maker = ConfigMaker(6830 + machine_number)

    # The result is on the following format
    # [server_ip]_[server_msgr_tcp_port]
    result = discovery_client.find_server(3)

    if result is None:
        return
    # Ip and tcp messenger port of the network hosting machine
    ip, port = result
    port = int(port)

    print("Server Addr:", ip, " MSG:", port)
    controller = ControllerMachineRx(ip, port)

    controller.connect_to_command_server()
    print("Controller will be ready, and will be killed when remote end requests")
    # Wait the thread until it terminates
    controller.start_controller(config_maker.get_ip(), config_maker.get_controller_port())
    controller.wait_till_terminate_requested()


if __name__ == "__main__":
    test()
