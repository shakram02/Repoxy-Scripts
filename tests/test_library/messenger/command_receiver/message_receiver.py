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


class PoxWrapper:
    def __init__(self, ip, port):
        self.running = False
        component = "l2_all_to_controller"
        self.runner = PoxRunner(ip, port, component)

    def launch_controller(self):
        if self.running is True:
            return
        self.runner.run_pox()
        self.running = True

    def kill_controller(self):
        if self.running is False:
            return
        self.runner.quit_pox()
        self.running = False


def get_machine_number():
    try:
        # 4 or 5
        return int(sys.argv[1])
    except IndexError:
        print "[Fallback to default machine number {4}]"
        return 4


def create_and_start_listener_socket(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((ip, port))
    server.listen(1)

    return server


def main():
    global OPEN_SOCKETS

    machine_number = get_machine_number()

    ip = '192.168.1.24{}'.format(machine_number)
    messenger_bind_port = MESSENGER_PORT_BASE + int(machine_number)
    controller_port = CONTROLLER_PORT_BASE + machine_number

    server = create_and_start_listener_socket(ip, messenger_bind_port)
    OPEN_SOCKETS.append(server)

    log('Listening on {}:{}'.format(ip, messenger_bind_port))
    client_sock, address = server.accept()
    OPEN_SOCKETS.append(client_sock)
    log('Accepted connection from {}:{}'.format(address[0], address[1]))

    pox_wrapper = PoxWrapper(ip, controller_port)

    while True:
        # Convert data to string, we don't need binary tides
        data = str(client_sock.recv(64)).strip()

        if len(data) == 0:
            break
        # Splin by \r\n
        print 'Received {}'.format(data)

        if data == "EXIT":
            break

        elif data == "EXEC":
            log("Launching POX")
            pox_wrapper.launch_controller()

        elif data == "KILL":
            log("Killing POX")
            pox_wrapper.kill_controller()
            log("POX is now down")

    log("Killing POX on termination")
    pox_wrapper.kill_controller()
    log('Closing sockets')
    server.shutdown(socket.SHUT_RDWR)
    server.close()
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()
    log('Sockets closed')


if __name__ == "__main__":
    try:
        import os
        import sys

        sys.path.insert(0, os.path.abspath(os.path.join(os.path.expanduser("~"), 'pox')))
        main()
    finally:
        # Close all open sockets
        for s in OPEN_SOCKETS:
            s.close()
