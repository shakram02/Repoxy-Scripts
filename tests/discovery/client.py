from __future__ import print_function
from socket import *
from messages import DISCOVER_PREFIX


class DisocveryClient(object):
    def __init__(self, port, disc_timeout=5, address='255.255.255.255'):
        self._server_address = (address, port)
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._sock.settimeout(disc_timeout)

    def find_server(self):
        try:
            while True:
                # Send data
                sent = self._sock.sendto(DISCOVER_PREFIX.encode(), self._server_address)

                if sent == -1:
                    return

                # Receive response
                data, server = self._sock.recvfrom(4096)
                msg = data.decode('UTF-8')
                if msg.startswith(DISCOVER_PREFIX):
                    return server, msg.replace(DISCOVER_PREFIX, "", 1)
        finally:
            self._sock.close()


def main():
    client = DisocveryClient(9434)
    addr = client.find_server()
    print("Found server with address:", addr)
    pass


if __package__ is None:
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

if __name__ == "__main__":
    main()
