import socket
from pox_runner import PoxRunner

OPEN_SOCKETS = []
MESSENGER_PORT_BASE = 6930
CONTROLLER_PORT_BASE = 6830

BLUE_BACKGROUND_BRIGHT = "\033[0;104m"
WHITE_BOLD = "\033[1;37m"
RESET = "\033[0m"


def log(string):
    print "{}{}[{}]{}".format(BLUE_BACKGROUND_BRIGHT, WHITE_BOLD, string, RESET)


def get_bind_address_info(machine_number):
    # TODO: don't hardcode, create config file
    ip = '192.168.1.24{}'.format(machine_number)
    port = MESSENGER_PORT_BASE + int(machine_number)
    return ip, port


def test_controller_launch(ip, port):
    import time

    log("Launching POX")

    component = "l2_all_to_controller"
    runner = PoxRunner(ip, port, component)
    runner.run_pox()
    time.sleep(2)

    log("Killing POX")
    runner.quit_pox()
    log("POX is now down")


def get_machine_number():
    try:
        # 4 or 5
        return sys.argv[1]
    except IndexError:
        print "[Fallback to default machine number {4}]"
        return 4


def create_and_start_listener_socket(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((ip, port))
    server.listen(1)

    return server


def main():
    machine_number = get_machine_number()

    ip = '192.168.1.24{}'.format(machine_number)
    messenger_bind_port = MESSENGER_PORT_BASE + int(machine_number)
    controller_port = CONTROLLER_PORT_BASE + machine_number

    server = create_and_start_listener_socket(ip, messenger_bind_port)
    OPEN_SOCKETS.append(server)

    print 'Listening on {}:{}'.format(ip, messenger_bind_port)
    client_sock, address = server.accept()
    OPEN_SOCKETS.append(client_sock)
    print 'Accepted connection from {}:{}'.format(address[0], address[1])

    while True:
        # Convert data to string, we don't need binary tides
        data = str(client_sock.recv(64)).strip()

        if len(data) == 0:
            break

        print 'Received {}'.format(data)

        if data == "EXIT" or len(data) == 0:
            break

        if data != "EXEC":
            continue

        test_controller_launch(ip, controller_port)

    client_sock.close()
    server.close()


if __name__ == "__main__":
    try:
        import os
        import sys

        sys.path.insert(0, os.path.abspath(os.path.join(os.path.expanduser("~"), 'pox')))
        main()
    except KeyboardInterrupt:
        # Close all open sockets
        for s in OPEN_SOCKETS:
            s.close()
