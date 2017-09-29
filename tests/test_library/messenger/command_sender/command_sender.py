import socket

receivers = [("192.168.1.244", 6934), ("192.168.1.245", 6935)]
# receivers = [("0.0.0.0", 6934), ("0.0.0.0", 6935)]

EXIT_COMMAND = "EXIT"
KILL_CONTROLLER_COMMAND = "KILL"
LAUNCH_CONTROLLER_COMMAND = "EXEC"


def create_client(address):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(address)
    return client


def send_to_all(socket_list, command):
    for so in socket_list:
        so.send(command)


def terminate_gracefully(socket_list):
    send_to_all(socket_list, EXIT_COMMAND)
    for so in socket_list:
        so.shutdown(socket.SHUT_RDWR)
        so.close()


def send_command(command, receiver_socket):
    if not command.endswith("\n"):
        command = command + "\r\n"

    receiver_socket.send(command)


def main(socket_list):
    while True:
        command = str(raw_input('> ')).upper()

        if len(command) == 0 or command == "EXIT":
            terminate_gracefully(socket_list)
            break

        splits = command.split(' ')
        if len(splits) == 2:
            s_command = splits[0]
            s_index = int(splits[1])
            send_command(s_command, socket_list[s_index])
        else:
            [send_command(command, s) for s in socket_list]


if __name__ == "__main__":
    sockets = None
    try:
        sockets = [create_client(receiver) for receiver in receivers]

        print "[Connected]"
        for (i, x) in enumerate(receivers):
            print "[{}] {}".format(i, x)

        main(sockets)
    except KeyboardInterrupt:
        if sockets is not None:
            terminate_gracefully(sockets)
