from scapy import all as scapy
import read_ip_csv as ric
import datetime
import os
import numpy as np

# INTERFACE = sys.argv[1]
INTERFACE = 'Ethernet'
LOCAL_IPS = []
src_loc_count = {}
dst_loc_count = {}

def normalizeDict(input_dict):
    X = np.array([val for val in input_dict.values()])
    norm_1 = np.abs(X).sum()
    return {key : input_dict[key]/norm_1 for key in input_dict.keys()}

def updateDict(key, input_dict):
    if key in input_dict:
        input_dict[key] = 1
    else:
        input_dict[key] = input_dict[key]+1
    return input_dict

def snyf():
    while True:
        pkt = scapy.sniff(count =1, iface = INTERFACE)
        
        try:
            srcIP = pkt[0].getlayer("IP").src
            dstIP = pkt[0].getlayer("IP").dst

            srcCC = 'LOCAL' if srcIP in LOCAL_IPS else ric.getCountryCodeFromIP(srcIP)
            dstCC = 'LOCAL' if dstIP in LOCAL_IPS else ric.getCountryCodeFromIP(dstIP)

            updateDict(srcCC, src_loc_count)
            updateDict(dstCC, dst_loc_count)

            # print(srcIP, '\t', srcCC, '\t', dstIP, '\t', dstCC, '\t', datetime.datetime.now())
            print()
        except Exception as e: 
            print(e)

def setLocalIP():
    IPs = os.popen('ipconfig | findstr IPv4').read().split('\n')[:-1]
    for ip in IPs:
        LOCAL_IPS.append(ip.split(': ')[1])
        

if __name__=='__main__':
    setLocalIP()
    snyf()