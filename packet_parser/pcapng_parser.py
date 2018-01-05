from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import rdpcap, Ether
from scapy.utils import PcapReader

from packet_parser.of_scapy import OpenFlow


def main():
    pcap = PcapReader('/mnt/Exec/code/research/ping-all.pcap')

    """

     Network 45306 -> Id [2]
        [ControllerRegion] ConnId [2] -> 48778 On controller
        [ReplicaRegion] ConnId [2] -> 38324 On controller

     Network 45308 -> Id [3]
         [ControllerRegion] ConnId [3] -> 48782 On controller
         [ReplicaRegion] ConnId [3] -> 38328 On controller
    """

    ports = {
        6833: "Proxy",
        6834: "Main Controller",
        6835: "Replicated Controller"
    }

    from scapy.packet import Raw

    for a in pcap.read_all():
        # print(a.__dict__)
        # print(repr(a))
        if isinstance(a.payload.payload, TCP):
            if hasattr(a, 'load'):
                of_packet = OpenFlow(a, a.load, ports.keys())
                print(repr(of_packet))

        # tcp_packet = TCP(a)
        # a = OpenFlow(tcp_packet, tcp_packet.load, [6833, 6834, 6835])
        # tcp_packet: TCP = a
        # ip_packet: IP = tcp_packet.payload


if __name__ == "__main__":
    main()
