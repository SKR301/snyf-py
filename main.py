from scapy import all as scapy

scapy.sniff(iface="Ethernet", prn = lambda x: x.summary())