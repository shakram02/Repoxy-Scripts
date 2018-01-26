from __future__ import print_function
from os import system
from entities.controller_machine import ControllerTx
from entities.mininet_machine import MininetMachine
from entities.networking.constants import DISCOVERY_PORT
from entities.networking.discovery_server import DiscoveryServer
from entities.networking.tcp_channel import TcpServer
from entities.networking.utils import get_ip, colorize

from optparse import OptionParser
from entities.protocol import SERVER_PORT
from connection_config import ConfigEntry, get_entry

parser = OptionParser()

parser.add_option("-c", "--clients", action="store", type="int", dest="client_count", default=1,
                  help="Number of controllers")

parser.add_option("-d", "--devices", action="store", type="int", dest="device_count", default=2,
                  help="Number of devices (hosts) attached to each switch")

parser.add_option("-s", "--switches", action="store", type="int", dest="switch_count", default=2,
                  help="Number of switches in network")

parser.add_option("-i", "--ip", action="store", type="string", dest="proxy_ip",
                  default=get_entry(ConfigEntry.ProxyIp),
                  help="Mininet controller (proxy) IP, default val in config.json")

parser.add_option("-p", "--port", action="store", type="string", dest="proxy_port",
                  default=get_entry(ConfigEntry.ProxyPort),
                  help="Mininet controller (proxy) Port, default val in config.json")


def test():
    (options, args) = parser.parse_args()
    client_count = options.client_count
    switch_count = options.switch_count
    device_count = options.device_count
    proxy_ip = options.proxy_ip
    proxy_port = options.proxy_port

    system('sudo mn -c > /dev/null 2>&1')  # Clean old mininet runs without showing output to screen.

    print(colorize("Server started, waiting {} clients...".format(client_count)))
    server = DiscoveryServer(DISCOVERY_PORT, client_count)
    tcp_server = TcpServer(get_ip(), SERVER_PORT)

    server.start(SERVER_PORT)
    clients = server.get_clients()
    print(colorize("Clients:{}".format(clients)))

    txs = []

    for i in range(client_count):
        socket = tcp_server.accept()
        tx = ControllerTx(socket)
        txs.append(tx)

    for tx in txs:
        print(colorize("Waiting controller to be ready..."))
        tx.wait_ready()

    print(colorize("Controllers ready, Running mininet..."))
    machine = MininetMachine()

    print(colorize("Mininet connecting to {}:{}".format(proxy_ip, proxy_port)))
    machine.start(switch_count, device_count, proxy_ip, int(proxy_port))

    hosts = machine.get_hosts()
    for host in hosts:
        for dest in hosts:
            if host == dest:
                continue
            # Ping pair
            machine.ping_hosts([host, dest])

    machine.terminate()
    print("Mininet Done...")

    for tx in txs:
        tx.kill_controller()

    tcp_server.close()
    print("Done...")


if __name__ == "__main__":
    test()
