from mininet_topology.create_and_run_network import create_network, dumpNodeConnections
from mininet import clean
from messenger.command_sender.message_sender import create_client, send_command
from messenger.command_receiver.protocol_messages import *


def create_mininet_network():
    clean.cleanup()
    net = create_network()
    return net


def start_network(net):
    dumpNodeConnections(net.hosts)
    net.start()


def stop_network(net):
    net.stop()
    clean.cleanup()


def mininet_clean():
    clean.cleanup()


def start_controller(socket):
    _send_to_receiver(PROTO_LAUNCH, socket)


def stop_controller(socket):
    _send_to_receiver(PROTO_SHUT_DOWN, socket)


def stop_tcp_messenger(socket):
    _send_to_receiver(PROTO_EXIT, socket)


def create_tcp_messenger(ip, port):
    return create_client((ip, port))


def ping_all(net):
    net.pingAll()


def _send_to_receiver(command, socket):
    if type(socket) is list:
        raise TypeError("Should get a single socket")

    send_command("{}".format(command), socket)
