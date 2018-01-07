from scapy.utils import PcapReader

from packet_parser.of_scapy import OpenFlow


class ConnectionTriplet(object):
    def __init__(self, net_src, to_main, to_repl, con_id):
        self.con_id = con_id
        self.net_src = net_src
        self.to_main = to_main
        self.to_repl = to_repl

    def __eq__(self, other):
        return self.net_src == other.net_src

    def __hash__(self):
        return self.con_id

    def __contains__(self, item):
        return item == self.net_src


def filter_control_packets(unfiltered):
    proto_packets = []
    # Reads packets in PCAP file, packets are read as TCP
    # because I'm using non-standard OpenFlow ports (default is 6653)
    for packet in unfiltered:
        flags = packet.sprintf('%TCP.flags%')

        # Ignore SYN, ACK only, FIN, RST packets
        if any([x in ['S', 'F', 'R'] for x in flags]) or flags == "A":
            # Ignore control packets
            continue

        proto_packets.append(packet)

    return proto_packets


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

    con_ids = {
        45306: 2,  # SRC
        48778: 2,  # DST
        38324: 2,  # DST

        45308: 3,
        48782: 3,
        38328: 3
    }

    ports = {
        6833: "Proxy",
        6834: "Main Controller",
        6835: "Replicated Controller"
    }

    ips = {
        "192.168.1.244": "Main Controller",
        "192.168.1.245": "Replicated Controller",
        "192.168.1.104": "Proxy",
        "192.168.1.241": "Network",
    }

    packet_list = filter_control_packets(pcap.read_all())

    for packet in packet_list:
        def get_id(sport, dport):
            if sport in con_ids:
                return con_ids[sport]
            if dport in con_ids:
                return con_ids[dport]
            raise KeyError("Invalid port")

        src = ips[packet['IP'].src]
        dst = ports[packet['TCP'].dport]
        con_id = get_id(packet['TCP'].sport, packet['TCP'].dport)

        print(packet.name, "From", src, "To", dst, "[{}]".format(con_id), " at", packet.time)


if __name__ == "__main__":
    main()
