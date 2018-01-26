#!/usr/bin/python
from __future__ import print_function

from entities.networking.utils import colorize
from mininet.node import RemoteController, DefaultController


class ComplexTopo:
    """
    mininet> py dumpNodeConnections(net.hosts)
    h1 h1-eth0:s1-eth1
    h3 h3-eth0:s2-eth1
    h4 h4-eth0:s2-eth2
    h2 h2-eth0:s1-eth2
    """

    def __init__(self, net, switch_count, hosts_per_switch, controller_ip, controller_port):
        self.net = net
        self.switch_count = switch_count
        self.hosts_per_switch = hosts_per_switch
        self.controller = self._create_controller(controller_ip, controller_port)
        self._switches = []
        self._hosts = []

    def build_network(self):
        self.net.addController(self.controller)
        self._create_network()
        self._connect_switches()
        self._connect_controller_to_switches()

    def _create_network(self, ):
        for i in range(self.switch_count):
            s = self.net.addSwitch('s{}'.format(i))
            self._switches.append(s)

            for j in range(self.hosts_per_switch):
                # This basically creates host with a seriesed numbers 0,1,2,...etc
                # without restting the count in each loop
                h = self.net.addHost('h{}'.format(j + (i * self.hosts_per_switch)))
                self._hosts.append(h)

                print(colorize("Adding:{} to {}".format(h.name, s.name)))
                self.net.addLink(s, h)

    def _connect_switches(self):
        for i in range(len(self._switches) - 1):
            s = self._switches[i]
            sn = self._switches[i + 1]
            print(colorize("Connecting:{} to {}".format(s.name, sn.name)))
            self.net.addLink(s, sn)

    def _connect_controller_to_switches(self):
        for s in self._switches:
            s.start([self.controller])

    def get_hosts(self):
        return self._hosts[:]

    @staticmethod
    def _create_controller(controller_ip, controller_port):
        if controller_ip in ["localhost", "127.0.0.1", "0.0.0.0"]:
            return DefaultController('c0', ip=controller_ip, port=controller_port)

        return RemoteController('c0', ip=controller_ip, port=controller_port)
