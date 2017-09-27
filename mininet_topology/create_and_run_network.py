#!/usr/bin/python
from mininet import clean
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.util import dumpNodeConnections

from complex_topology import ComplexTopo
import sys

defaults = {
    "proxy_ip": "192.168.1.248",
    "proxy_port": "6833",
    "switch_count": "8",
    "hosts_per_switch": "2",
}


def try_get_arg(index, key):
    # TODO: use docopt
    try:
        return sys.argv[index]
    except IndexError:
        return defaults[key]


def create_network(proxy_ip="192.168.1.248", proxy_port=6833, switch_count=8, hosts_per_switch=2):
    net = Mininet()
    topo = ComplexTopo(net, switch_count, hosts_per_switch, proxy_ip, proxy_port)
    topo.build_network()

    return net


def main():
    global network

    clean.cleanup()
    setLogLevel('info')

    proxy_ip = try_get_arg(1, "proxy_ip")
    proxy_port = int(try_get_arg(2, "proxy_port"))
    switch_count = int(try_get_arg(3, "switch_count"))
    hosts_per_switch = int(try_get_arg(4, "hosts_per_switch"))

    network = create_network(proxy_ip, proxy_port, switch_count, hosts_per_switch)
    network.start()

    print "[Showing connections]"
    dumpNodeConnections(network.hosts)
    print "[Testing network]"
    network.pingAll()
    network.stop()


if __name__ == "__main__":
    network = None
    try:
        main()
    except KeyboardInterrupt:
        if network is not None:
            network.stop()
    finally:
        clean.cleanup()
