from scapy import all as scapy
import sys

interface = sys.argv[1]
scapy.sniff(iface = interface, prn = lambda x: x.summary())