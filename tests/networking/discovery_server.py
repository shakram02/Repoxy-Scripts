from __future__ import print_function
import socket
import sys
from constants import DISCOVERY_PREFIX, DISCOVERY_PORT


class DiscoveryServer(object):
    def __init__(self, server_ip, port, count, timeout=5):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((server_ip, port))
        self._sock.settimeout(timeout)

        self._expected_count = count

    def start(self, max_try_count=-1, onreceive=None):
        try_count = 0
        connected = 0
        while connected < self._expected_count:
            try:
                data, address = self._sock.recvfrom(256)
            except socket.timeout:
                try_count += 1

                if try_count == max_try_count:
                    self.stop()
                    return

                continue

            data = str(data.decode('UTF-8'))
            connected += 1

            if onreceive is not None:
                onreceive(address, data.replace(DISCOVERY_PREFIX, "", 1))

            if data.startswith(DISCOVERY_PREFIX):
                sent = self._sock.sendto(DISCOVERY_PREFIX.encode(), address)
                if sent == -1:
                    self.stop()
                    return

    def stop(self):
        self._sock.close()


def try_get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


def main():
    print("Running networking server...")

    expected_clients = try_get_arg(1, 1)

    server = DiscoveryServer('', DISCOVERY_PORT, expected_clients)
    server.start(onreceive=lambda addr, data: print("Client:", addr, "Sent: [", data, "]"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Terminated...")
