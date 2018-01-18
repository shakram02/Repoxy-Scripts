from __future__ import print_function

import socket
from pox_runner import PoxRunner
from protocol_messages import *
from misc import colorize
from logging import basicConfig, DEBUG, getLogger, debug, error

OPEN_SOCKETS = []
MESSENGER_PORT_BASE = 6930
CONTROLLER_PORT_BASE = 6830


def get_machine_number():
    try:
        # 4 or 5
        return int(sys.argv[1])
    except IndexError:
        print("[Fallback to default machine number {4}]")
        return 4


def create_and_start_listener_socket(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(1)

    return server


def clean_up(pox_wrapper, server, client_sock):
    debug(colorize("Killing POX on termination"))
    pox_wrapper.shutdown_controller()
    debug(colorize('Closing sockets'))
    client_sock.close()
    server.close()
    debug(colorize('Sockets closed'))


def proto_process(item, controller_manager):
    # Split by \r\n
    print('Received {}'.format(item))

    if item == PROTO_LAUNCH:
        debug(colorize("Launching POX"))
        controller_manager.launch_controller()

    elif item == PROTO_SHUT_DOWN:
        debug(colorize("Shutting down POX"))
        controller_manager.shutdown_controller()
        debug(colorize("POX is now down"))

    elif item == PROTO_KILL or len(item) == 0:
        debug(colorize("Killing POX"))
        controller_manager.kill_controller()
        debug(colorize("Killed POX"))


def main(ip):
    global OPEN_SOCKETS

    server = create_and_start_listener_socket(ip, messenger_bind_port)
    OPEN_SOCKETS.append(server)

    debug(colorize('Listening on {}:{}'.format(ip, messenger_bind_port)))
    client_sock, address = server.accept()
    OPEN_SOCKETS.append(client_sock)
    debug(colorize('Accepted connection from {}:{}'.format(address[0], address[1])))

    terminated = False

    while not terminated:
        # Convert data to string, we don't need binary tides
        byte_count = client_sock.recv(64)

        if byte_count == -1:
            return

        data = str(client_sock.recv(64)).strip()
        data = data.split('\r\n')

        if len(data) == 0:
            print("Nothing received, Killing controller")
            return

        for item in data:
            debug(colorize("Command: {}".format(item)))
            if item == PROTO_EXIT or len(item) == 0:
                return

            item = item.strip().upper()
            proto_process(item, pox_runner)


if __name__ == "__main__":

    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.expanduser("~"), 'pox')))
    basicConfig(level=DEBUG)
    logger = getLogger(__name__)
    machine_number = get_machine_number()

    controller_ip = '192.168.1.24{}'.format(machine_number)
    messenger_bind_port = MESSENGER_PORT_BASE + machine_number

    controller_port = CONTROLLER_PORT_BASE + machine_number
    pox_runner = PoxRunner(controller_ip, controller_port)

    try:
        main(controller_ip)
    except Exception as e:
        error(e)
    finally:
        pox_runner.kill_controller()
        # Close all open sockets
        for s in OPEN_SOCKETS:
            s.close()
