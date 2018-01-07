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
     Network 33012 -> Id [2]
        [ControllerRegion] ConnId [2] -> 34178 On controller
        [ReplicaRegion] ConnId [2] -> 56438 On controller
     
     Network 33014 -> Id [3]
        [ControllerRegion] ConnId [3] -> 34182 On controller
        [ReplicaRegion] ConnId [3] -> 56442 On controller
    """

    con_ids = {
        33012: 2,  # SRC
        34178: 2,  # DST
        56348: 2,  # DST

        33014: 3,
        34182: 3,
        56442: 3
    }

    ports = {
        6833: "Proxy",
        6834: "Main Controller",
        6835: "Replicated Controller"
    }
    custom_ports = ports.keys()

    ips = {
        "192.168.1.244": "Main Controller",
        "192.168.1.245": "Replicated Controller",
        "192.168.1.104": "Proxy",
        "192.168.1.241": "Network",
    }

    packet_list = filter_control_packets(pcap.read_all())

    def get_id(sport, dport):
        if sport in con_ids:
            return con_ids[sport]
        if dport in con_ids:
            return con_ids[dport]

        return False

    for packet in packet_list:
        sport = packet['TCP'].sport
        dport = packet['TCP'].dport

        con_id = get_id(sport, dport)
        if not con_id: continue  # Invalid first test socket that pox opens

        src = ips[packet['IP'].src]
        dst = ips[packet['IP'].dst]

        of_packet = OpenFlow(packet, packet.load, custom_ports)
        print("[{}] [{}]".format(packet.time, of_packet.name), src, "-->", dst, "[{}]".format(con_id))


if __name__ == "__main__":
    main()
