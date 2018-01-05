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
    custom_ports = ports.keys()

    # Reads packets in PCAP file, packets are read as TCP
    # because I'm using non-standard OpenFlow ports (default is 6653)
    for packet in pcap.read_all():
        flags = packet.sprintf('%TCP.flags%')

        # Ignore SYN, ACK only, FIN, RST packets
        if any([x in ['S', 'F', 'R'] for x in flags]) or flags == "A":
            # Ignore control packets
            continue

        # packet.load yields OF packet as bytes
        of_packet = OpenFlow(packet, packet.load, custom_ports)

        print(of_packet.name, "From", packet['IP'].src, "To", ports[packet['TCP'].dport])


if __name__ == "__main__":
    main()
