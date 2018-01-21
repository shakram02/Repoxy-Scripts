from constants import UDP_ACK, DISCOVERY_TIMEOUT
from socket import socket, timeout, SO_BROADCAST, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM, AF_INET


class UdpChannel(object):
    def __init__(self, ip, port):
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._sock.settimeout(DISCOVERY_TIMEOUT)
        self._sock.bind((ip, port))

    def send(self, msg, ip, port):
        sent = self._sock.sendto(msg, (ip, port))

        if sent == -1:
            raise ConnectionError("Socket error")

        # Receive response, blocks
        try:
            data, _ = self._sock.recvfrom(256)
        except timeout:
            return None

        if data == UDP_ACK:
            return True
        else:
            raise AttributeError("Invalid ACK {}".format(data))

    def recv(self):
        try:
            data, addr = self._sock.recvfrom(256)
            self._sock.sendto(UDP_ACK, addr)
            return data
        except timeout:
            return None


def recv_th(port):
    ch = UdpChannel("localhost", port + 1)

    print("Waiting...")
    while True:
        val = ch.recv()
        if val is None:
            continue
        else:
            break

    print("Done...")


def test(port):
    from threading import Thread
    from time import sleep
    th = Thread(target=recv_th, args=(port,))
    th.start()
    sleep(1.5)
    sender = UdpChannel("localhost", port)
    result = sender.send(bytes([123, 111]), "localhost", port + 1)
    print("Result:", result)
    sleep(0.5)
    th.join()


if __name__ == "__main__":
    TEST_PORT = 61011
    test(TEST_PORT)
