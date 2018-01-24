from networking import DiscoveryServer
from networking import DISCOVERY_PORT
from entities.controller_machine import ControllerTx


def test():
    print("Server started")
    server = DiscoveryServer(DISCOVERY_PORT, 1)
    server.start(6633)
    clients = server.get_clients()

    print("Clients:", clients)

    controller = ControllerTx()
    controller.open_connection(clients[0], 6633)

    print("waiting for ready")
    controller.wait_ready()

    print("Send kill")
    controller.kill_controller()


if __name__ == "__main__":
    test()
