from entities.controller_machine import ControllerTx
from entities.networking.constants import DISCOVERY_PORT
from entities.networking.discovery_server import DiscoveryServer
from entities.networking.tcp_channel import TcpServer
from entities.networking.utils import get_ip
from entities.protocol import SERVER_PORT


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

    print("Controllers ready...")

    # TODO run mininet here
    print("Run mininet...")

    for tx in txs:
        tx.kill_controller()

    from time import sleep
    print("Waiting a little bit")
    sleep(4)
    tcp_server.close()
    print("Done...")


if __name__ == "__main__":
    test()
