import socket


class ControllerFeedbackListener:
    def __init__(self, listen_ip, listen_port):
        self._ip = listen_ip
        self._port = listen_port
        self._client = None

        self._srver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._srver_socket.bind((self._ip, self._port))
        self._srver_socket.listen(1)

    def accept_client(self, timeout):
        self._srver_socket.settimeout(timeout)  # timeout for accepting
        self._client, addr = self._srver_socket.accept()
        return addr

    def wait_for_message(self, timeout, buffer_size=128):
        self._srver_socket.settimeout(timeout)  # timeout for accepting
        msg = self._client.recv(buffer_size).decode()
        return msg

    def close_connection(self):
        self._srver_socket.close()
        # Client will close their socket
