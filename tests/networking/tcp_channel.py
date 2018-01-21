from socket import socket, timeout, SOL_SOCKET, SO_REUSEADDR, SOCK_STREAM, AF_INET

from constants import DISCOVERY_TIMEOUT


class TcpClient(object):
    def __init__(self):
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._sock.settimeout(DISCOVERY_TIMEOUT)

    def connect(self, ip, port):
        """
        Connect to remote end
        :param ip: Ip
        :param port: Port
        """
        address = (ip, port)
        self._sock.connect(address)

    def send(self, msg):
        if isinstance(msg, (bytes, bytearray)):
            sent = self._sock.send(msg)
        else:
            sent = self._sock.send(bytes(msg, "UTF-8"))

        if sent == -1:
            raise ConnectionError("Socket error")

    def recv(self):
        try:
            data, _ = self._sock.recv(256)
            return data
        except timeout:
            return None

    def close(self):
        self._sock.close()


class TcpServer(object):
    def __init__(self, ip, port, socket_timeout=5):
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._sock.settimeout(socket_timeout)
        self._sock.bind((ip, port))
        self._sock.listen()
        self._client = None
        self.client_addr = None

    def accept(self):
        self._client, self.client_addr = self._sock.accept()

    def send(self, msg):
        if isinstance(msg, (bytes, bytearray)):
            sent = self._client.send(msg)
        else:
            sent = self._client.send(bytes(msg, "UTF-8"))

        if sent == -1:
            raise ConnectionError("Socket error")

    def recv(self):
        try:
            data = self._client.recv(256)
        except timeout:
            return None
        return data

    def close(self):
        self._client.close()
        self._sock.close()


def recv_th(port):
    ch = TcpServer("localhost", port + 1)

    print("Accepting...")
    ch.accept()

    print("Waiting for message...")
    while True:
        val = ch.recv()
        if val is None:
            continue
        else:
            print("Recv (bytes/text):", val.decode("UTF-8"))
            break

    print("Done...")


def test(port):
    from threading import Thread
    from time import sleep
    th = Thread(target=recv_th, args=(port,))
    th.start()
    sleep(1)

    sender = TcpClient()
    sender.connect("localhost", port + 1)
    sender.send("asdas")

    sleep(1.5)
    th.join()


if __name__ == "__main__":
    TEST_PORT = 61011
    test(TEST_PORT)
