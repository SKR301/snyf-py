from scapy import all as scapy
import read_ip_csv as ric
import datetime
import os

# INTERFACE = sys.argv[1]
INTERFACE = 'Ethernet'
LOCAL_IPS = []

def snyf():
    while True:
        pkt = scapy.sniff(count =1, iface = INTERFACE)
        
        try:
            srcIP = pkt[0].getlayer("IP").src
            dstIP = pkt[0].getlayer("IP").dst

            srcCC = 'LOCAL' if srcIP in LOCAL_IPS else ric.getCountryCodeFromIP(srcIP)
            dstCC = 'LOCAL' if dstIP in LOCAL_IPS else ric.getCountryCodeFromIP(dstIP)

            print(srcIP, '\t', srcCC, '\t', dstIP, '\t', dstCC, '\t', datetime.datetime.now())
        except Exception:
            print()

def setLocalIP():
    IPs = os.popen('ipconfig | findstr IPv4').read().split('\n')[:-1]
    for ip in IPs:
        LOCAL_IPS.append(ip.split(': ')[1])
        

if __name__=='__main__':
    setLocalIP()
    snyf()