from mininet import clean
from mininet.net import Mininet
from mininet_topo.complex_topology import ComplexTopo


class MininetMachine(object):
    def __init__(self):
        # TODO: initialize discovery
        self._net = None

    def start(self, switch_count, hosts_per_switch, ip, port):
        """
        Creates mininet network
        :param switch_count: Number of switches in network
        :param hosts_per_switch: Hosts per every switch
        :param ip: Controller IP
        :param port: Controller Port
        :return Created network object
        """
        self._clean()
        self._net = Mininet()
        topo = ComplexTopo(self._net, switch_count, hosts_per_switch, ip, port)
        topo.build_network()

    def ping(self):
        self._net.pingAll()

    def terminate(self):
        self._net.stop()

    @staticmethod
    def _clean():
        clean.cleanup()
