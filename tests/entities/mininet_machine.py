from mininet import clean
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet_topo.complex_topology import ComplexTopo


class MininetMachine(object):
    def __init__(self):
        # TODO: initialize discovery
        self._net = None

    def start(self, switch_count, hosts_per_switch, controller_ip, controller_port, topo=None):
        """
        Creates mininet network
        :param topo: Network topology for mininet
        :param switch_count: Number of switches in network
        :param hosts_per_switch: Hosts per every switch
        :param controller_ip: Controller IP
        :param controller_port: Controller Port
        :return Created network object
        """
        self._clean()

        if topo is None:
            self._net = Mininet()
            topo = ComplexTopo(self._net, switch_count, hosts_per_switch, controller_ip, controller_port)
            topo.build_network()
        else:
            self._net = Mininet(topo=topo)

        self._net.start()

    def ping(self):
        self._net.pingAll()

    def terminate(self):
        self._net.stop()

    @staticmethod
    def _clean():
        clean.cleanup()


def test():
    machine = MininetMachine()
    machine.start(2, 1, "localhost", 6633, TreeTopo(depth=1, fanout=2))
    machine.ping()
    machine.terminate()
    print("Done...")


if __name__ == "__main__":
    test()
