import datetime
import socket
import numpy as np
import matplotlib.pyplot as plt
import dpkt

f = open('/mnt/Exec/code/research/filtered_capture.pcap')
pcap = dpkt.pcap.Reader(f)
count = 0

main_controller = []
sec_controller = []
to_network = []

min_time = None
max_time = None

# For each packet in the pcap process the contents
for timestamp, buf in pcap:
    count += 1

    micros = datetime.datetime.utcfromtimestamp(timestamp).microsecond

    min_time = micros if min_time is None else min(min_time, micros)
    max_time = micros if max_time is None else max(max_time, micros)

    # Print out the timestamp in UTC
    print 'Timestamp: ', str(micros)

    # Unpack the Ethernet frame (mac src/dst, ethertype)
    eth = dpkt.ethernet.Ethernet(buf)
    # print 'Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type

    # Make sure the Ethernet frame contains an IP packet
    if not isinstance(eth.data, dpkt.ip.IP):
        print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
        continue

    # Now unpack the data within the Ethernet frame (the IP packet)
    # Pulling out src, dst, length, fragment info, TTL, and Protocol
    ip = eth.data

    # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
    do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
    more_fragments = bool(ip.off & dpkt.ip.IP_MF)
    fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

    tcp = ip.data

    # Print out the info
    print 'IP: %s:%s -> %s:%s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
          (socket.inet_ntoa(ip.src), tcp.sport, socket.inet_ntoa(ip.dst), tcp.dport, ip.len, ip.ttl, do_not_fragment,
           more_fragments, fragment_offset)

    if tcp.sport == 6833:
        to_network.append(tcp)
    elif tcp.sport == 6834:
        main_controller.append(tcp)
    elif tcp.sport == 6835:
        sec_controller.append(tcp)

print "Count:%s" % count

t = np.arange(min_time / 1000000.0, max_time / 1000000.0, 0.05)

# red dashes, blue squares and green triangles
plt.plot(t, t ** 3, 'r', t, t ** 2, 'b')
plt.show()
