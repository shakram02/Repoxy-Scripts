from __future__ import print_function
from socket import socket, timeout, SO_BROADCAST, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM, AF_INET

import sys

from constants import DISCOVERY_PREFIX, DISCOVERY_PORT, DISCOVERY_TIMEOUT


class DiscoveryClient(object):
    """
    Tries to reach a DiscoveryServer to get the TCP port to open connection to
    """

    def __init__(self, port, disc_timeout=DISCOVERY_TIMEOUT, address='255.255.255.255'):
        self._server_address = (address, port)
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._sock.settimeout(disc_timeout)

    def find_server(self, retry_count=-1):
        count = 0
        while count < retry_count or retry_count == -1:
            count += 1

            try:
                # Send data
                sent = self._sock.sendto(DISCOVERY_PREFIX.encode(), self._server_address)
                if sent == -1:
                    raise ConnectionError("Socket crashed")

                # Receive response, blocks
                data, server = self._sock.recvfrom(256)

                # Received data
                msg = data.decode('UTF-8')
                self._sock.close()

                if msg.startswith(DISCOVERY_PREFIX):
                    server_ip, _ = server  # Drop sender port
                    # The server reply must contain tcp port
                    return server_ip, msg.replace(DISCOVERY_PREFIX, "", 1)
                else:
                    raise ConnectionError("Invalid identification message {}".format(msg))
            except timeout:
                print("Retrying to connect...", file=sys.stderr)
                continue


def main():
    client = DiscoveryClient(DISCOVERY_PORT)
    addr = client.find_server()
    print("Found server with address:", addr)
    pass


if __name__ == "__main__":
    main()
