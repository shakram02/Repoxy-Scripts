import socket
import automation_functions as af


class TestMachine:
    def __init__(self, ip, messenger_port, controller_port):
        self.ip = ip
        self.messenger_port = messenger_port
        self.controller_port = controller_port

        self.messenger_socket = socket.socket
        self._controller_launched = False
        self._create_messenger()

    def _create_messenger(self):
        self.messenger_socket = af.create_tcp_messenger(self.ip, self.messenger_port)

    def start_controller(self):
        if self._controller_launched:
            return
        af.start_controller(self.messenger_socket)
        self._controller_launched = True

    def stop_controller(self):
        if not self._controller_launched:
            return

        af.stop_controller(self.messenger_socket)
        self._controller_launched = False

    def kill_controller(self):
        if not self._controller_launched:
            return
        af.kill_controller(self.messenger_socket)
        self._controller_launched = False

    def _stop_messenger(self):
        af.stop_tcp_messenger(self.messenger_socket)
        self._controller_launched = False

    def shutdown(self):
        if self._controller_launched:
            self.stop_controller()
        self._stop_messenger()
