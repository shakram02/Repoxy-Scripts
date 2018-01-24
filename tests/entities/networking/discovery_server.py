from __future__ import print_function
import socket
import sys
from constants import DISCOVERY_PREFIX, DISCOVERY_PORT, DISCOVERY_TIMEOUT


class DiscoveryServer(object):
    """
    Receives UDP broadcasts to figure out client IPs, each caught client will be
    sent a TCP port to open a connection with and then exchange data reliably through
    """

    def __init__(self, server_port, count, timeout=DISCOVERY_TIMEOUT):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(('', server_port))
        self._sock.settimeout(timeout)

        self._expected_count = count
        self._clients = []

    def start(self, tcp_port=0, max_try_count=-1, onreceive=None):
        try_count = 0
        connected = 0
        while connected < self._expected_count:
            try:
                data, address = self._sock.recvfrom(256)
                data = str(data.decode('UTF-8'))

                if not data == DISCOVERY_PREFIX:
                    raise AssertionError("Invalid Identification message {}".format(data))

            except socket.timeout:
                try_count += 1

                if try_count == max_try_count:
                    self.stop()
                    return
                continue

            # Update state
            connected += 1
            client_ip = address[0]  # Ignore client port, it's meaningless
            self._clients.append(client_ip)

            if onreceive is not None:
                onreceive(address)

            # Reply with TCP port
            sent = self._sock.sendto((DISCOVERY_PREFIX + str(tcp_port)).encode(), address)
            if sent == -1:
                self.stop()
                raise ConnectionError("Socket crashed")

    def get_clients(self):
        return self._clients

    def stop(self):
        self._sock.close()


def try_get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


def main():
    print("Running networking server...")
    tcp_port = 6011  # Port to open TCP connection with
    expected_clients = try_get_arg(1, 1)

    server = DiscoveryServer(DISCOVERY_PORT, expected_clients)
    server.start(tcp_port, onreceive=lambda addr: print("Client:", addr))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Terminated...")