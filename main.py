from scapy import all as scapy
import pygeoip
import datetime
import traceback
import sys
from os import system
import geopandas as gpd

# interface = sys.argv[1]
interface = 'Ethernet'
GEO = pygeoip.GeoIP('GeoIP.dat')
heatMapSrcData = {}
heatMapDstData = {}

def getCountryFromIP(ip):
    return GEO.country_name_by_addr(ip)

while True:
    pkt = scapy.sniff(count =1, iface = interface)
    
    try:
        srcIP = pkt[0].getlayer("IP").src
        dstIP = pkt[0].getlayer("IP").dst

        srcCountry = 'India' if srcIP[:3] == '192' else getCountryFromIP(srcIP)
        dstCountry = 'India' if dstIP[:3] == '192' else getCountryFromIP(dstIP)

        if srcCountry in heatMapSrcData:
            heatMapSrcData[srcCountry] = heatMapSrcData[srcCountry]+1
        else:
            heatMapSrcData[srcCountry] = 1
        
        if dstCountry in heatMapDstData:
            heatMapDstData[dstCountry] = heatMapDstData[dstCountry]+1
        else:
            heatMapDstData[dstCountry] = 1

        # print(srcIP, ':', srcCountry, '-', dstIP, ':', dstCountry, '[', datetime.datetime.now(), ']')
        # print('src:\t', heatMapDstData)
        # print('dst:\t', heatMapSrcData)

    except Exception:
        print(traceback.format_exc())
        print()