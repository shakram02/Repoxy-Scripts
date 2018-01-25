from __future__ import print_function
from entities.controller_machine import ControllerTx
from entities.mininet_machine import MininetMachine
from entities.networking.constants import DISCOVERY_PORT
from entities.networking.discovery_server import DiscoveryServer
from entities.networking.tcp_channel import TcpServer
from entities.networking.utils import get_ip, colorize

from entities.protocol import SERVER_PORT
from connection_config import ConfigEntry, get_entry


def test():
    try:
        import sys
        client_count = int(sys.argv[1])
    except IndexError:
        client_count = 1

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

    # TODO run mininet here
    print(colorize("Controllers ready, Run mininet..."))

    proxy_ip = get_entry(ConfigEntry.ProxyIp)
    proxy_port = get_entry(ConfigEntry.ProxyPort)
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
