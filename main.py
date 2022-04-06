from scapy import all as scapy
import sys

interface = sys.argv[1]
while True:
    pkt = scapy.sniff(count =1, iface = interface, prn = lambda x: x.summary())
    
    try:
       srcIP = pkt[0].getlayer("IP").src
       dstIP = pkt[0].getlayer("IP").dst
    except:
        print()