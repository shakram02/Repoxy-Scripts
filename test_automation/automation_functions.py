from mininet_topology.create_and_run_network import create_network, dumpNodeConnections
from mininet import clean
from messenger.command_sender.command_sender import create_client, send_command
from messenger.command_sender.command_sender import KILL_CONTROLLER_COMMAND, LAUNCH_CONTROLLER_COMMAND, EXIT_COMMAND


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


def launch_controllers(client_sockets):
    _send_to_all_receivers(LAUNCH_CONTROLLER_COMMAND, client_sockets)


def launch_controller(controller_id, socket):
    _send_to_receiver(LAUNCH_CONTROLLER_COMMAND, controller_id, socket)


def stop_controllers(client_sockets):
    _send_to_all_receivers(KILL_CONTROLLER_COMMAND, client_sockets)


def stop_controller(controller_id, socket):
    _send_to_receiver(KILL_CONTROLLER_COMMAND, controller_id, socket)


def start_tcp_messenger(ip, port):
    return create_client((ip, port))


def stop_tcp_messenger(controller_id, socket):
    _send_to_receiver(EXIT_COMMAND, controller_id, socket)


def ping_all(net):
    net.pingAll()


def _send_to_receiver(command, controller_id, socket):
    if type(socket) is list:
        raise TypeError("Should get a single socket")

    send_command("{} {}".format(command, controller_id), [socket])


def _send_to_all_receivers(command, sockets):
    if type(sockets) is not list:
        raise TypeError("Should get a list of sockets")

    for (i, s) in enumerate(sockets):
        _send_to_receiver(command, i, s)
