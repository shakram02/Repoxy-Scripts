from entities.controller_machine import ControllerTx
from entities.mininet_machine import MininetMachine
from entities.networking.constants import DISCOVERY_PORT
from entities.networking.discovery_server import DiscoveryServer
from entities.networking.tcp_channel import TcpServer
from entities.networking.utils import get_ip
from entities.protocol import SERVER_PORT
from settings import ConfigEntry, get_entry


def test():
    client_count = 1
    print("Server started")
    server = DiscoveryServer(DISCOVERY_PORT, client_count)
    tcp_server = TcpServer(get_ip(), SERVER_PORT)

    server.start(SERVER_PORT)
    clients = server.get_clients()
    print("Clients:", clients)

    txs = []

    for i in range(client_count):
        socket = tcp_server.accept()
        tx = ControllerTx(socket)
        txs.append(tx)

    for tx in txs:
        print("Waiting controller to be ready...")
        tx.wait_ready()

    # TODO run mininet here
    print("Controllers ready, Run mininet...")

    proxy_ip = "192.168.1.248"
    proxy_port = 6833
    machine = MininetMachine()
    machine.start(2, 2, proxy_ip, proxy_port)
    machine.ping()
    machine.terminate()
    print("Mininet Done...")

    for tx in txs:
        tx.kill_controller()

    tcp_server.close()
    print("Done...")


if __name__ == "__main__":
    test()
