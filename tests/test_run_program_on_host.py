from mininet import clean
from mininet.log import setLogLevel

from test_library.mininet_topology.create_and_run_network import create_network


def main():
    clean.cleanup()
    setLogLevel('info')

    network = create_network(proxy_ip="192.168.1.244", proxy_port=6834, switch_count=3)
    network.start()
    network.pingAll()
    results = []

    for host in network.hosts:
        for rx_host in network.hosts:
            if host == rx_host:
                continue
            result_string = network.iperf((host, rx_host))
            results.append("{} | {} : {}".format(host, rx_host, result_string))

    # network.iperf((network.get('h1'), network.get('h2')))
    network.stop()
    clean.cleanup()


if __name__ == "__main__":
    main()
