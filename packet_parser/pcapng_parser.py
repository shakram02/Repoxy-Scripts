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


class ConversationPacket(object):
    def __init__(self, packet, ips, con_id, of_ports):
        self._packet = packet
        self._of_packet = OpenFlow(packet, packet.load, of_ports)
        self.packet_type = self._of_packet.name
        self.src = ips[packet['IP'].src]
        self.dst = ips[packet['IP'].dst]
        self.sport = packet['TCP'].sport
        self.dport = packet['TCP'].dport
        self.con_id = con_id
        self.time = packet.time

    def get_type(self):
        pass


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
    pcap = PcapReader('/mnt/Exec/code/research/ping-all-of-1.pcap')

    """
    Network 40576 -> Id [2]
        [ControllerRegion] ConnId [2] -> 59760 On controller
        [ReplicaRegion] ConnId [2] -> 36316 On controller
    
    Network 40578 -> Id [3]
        [ControllerRegion] ConnId [3] -> 59764 On controller
        [ReplicaRegion] ConnId [3] -> 36320 On controller
    """

    con_ids = {
        40576: 2,  # SRC
        59760: 2,  # DST
        36316: 2,  # DST
        #
        40578: 3,
        59764: 3,
        36320: 3
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
        "192.168.1.248": "Proxy",
        "192.168.1.136": "Proxy",
        "192.168.1.241": "Network",
    }

    packet_list = filter_control_packets(pcap.read_all())

    def get_id(sprt, dprt):
        if sprt in con_ids:
            return con_ids[sprt]
        if dprt in con_ids:
            return con_ids[dprt]

        return False

    packets = []
    for packet in packet_list:
        sport = packet['TCP'].sport
        dport = packet['TCP'].dport

        con_id = get_id(sport, dport)
        if not con_id:
            print("Skip", repr(packet))
            continue  # Invalid first test socket that pox opens

        p = ConversationPacket(packet, ips, con_id, custom_ports)
        packets.append(p)
        # src = ips[packet['IP'].src]
        # dst = ips[packet['IP'].dst]

        # of_packet = OpenFlow(packet, packet.load, custom_ports)
        # print("[{}] [{}]".format(p.time, p.packet_type), p.src, "-->", p.dst, "[{}]".format(p.con_id))

    print("Found", len(packet_list), "Packets [ACKs are ignored]")
    con_2 = [x for x in packets if x.con_id == 2]
    con_3 = [x for x in packets if x.con_id == 3]
    #
    # sorted(con_2, key=lambda x: x.time)
    # packets.sort(key=lambda x: x.con_id)
    # for p in packets:
    #     print("[{}] [{}]".format(p.time, "_"), p.src, "-->", p.dst, "[{}]".format(p.con_id))
    for i in range(int(len(con_2))):
        p = con_2[i]
        print("[{}] [{}]".format(p.time, p.packet_type), p.src, "-->", p.dst, "[{}]".format(p.con_id))


if __name__ == "__main__":
    main()
