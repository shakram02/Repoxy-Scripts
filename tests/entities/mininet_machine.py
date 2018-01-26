from mininet import clean
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.util import dumpNodeConnections
from mininet_topo.complex_topology import ComplexTopo


class MininetMachine(object):
    def __init__(self):
        self._net = None
        self._topo = None

    def start(self, switch_count, hosts_per_switch, controller_ip, controller_port):
        """
        Creates mininet network
        :param switch_count: Number of switches in network
        :param hosts_per_switch: Hosts per every switch
        :param controller_ip: Controller IP
        :param controller_port: Controller Port
        :return Created network object
        """
        self._clean()
        setLogLevel('info')

        self._net = Mininet()
        self._topo = ComplexTopo(self._net, switch_count, hosts_per_switch, controller_ip, controller_port)
        self._topo.build_network()

        dumpNodeConnections(self._net.hosts)
        self._net.start()

    def ping_all(self):
        self._net.pingAll()

    def terminate(self):
        self._net.stop()

    def ping_hosts(self, hosts):
        return self._net.ping(hosts)

    def get_hosts(self):
        return self._topo.get_hosts()

    @staticmethod
    def _clean():
        clean.cleanup()
