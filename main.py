from scapy import all as scapy
import pygeoip
import traceback
import sys

interface = sys.argv[1]
GEO = pygeoip.GeoIP('GeoIP.dat')

def getCountryFromIP(ip):
    return GEO.country_name_by_addr(ip)

while True:
    pkt = scapy.sniff(count =1, iface = interface)
    
    try:
        srcIP = pkt[0].getlayer("IP").src
        dstIP = pkt[0].getlayer("IP").dst

        print(srcIP,":",getCountryFromIP(srcIP),"-",dstIP,getCountryFromIP(dstIP))
    except Exception:
        # print(traceback.format_exc())
        print()