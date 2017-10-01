import socket


def create_client(address):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(address)
    return client


def send_to_all(socket_list, command):
    for so in socket_list:
        so.send(command)


def send_command(command, receiver_socket):
    if not command.endswith("\r\n"):
        command = command + "\r\n"

    receiver_socket.send(command)
