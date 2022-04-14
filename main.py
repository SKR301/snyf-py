from scapy import all as scapy
import read_ip_csv as ric
import datetime
import os
import multiprocessing
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib as mpl

# INTERFACE = sys.argv[1]
INTERFACE = 'Ethernet'
LOCAL_IPS = []
src_loc_count = {}
dst_loc_count = {}

cmap = mpl.cm.Blues
fig = plt.figure(figsize=(7.5, 5))
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
ax = plt.axes(projection=ccrs.PlateCarree())

def normalizeDict(input_dict):
    X = np.array([val for val in input_dict.values()])
    norm_1 = np.abs(X).sum()
    return {key : input_dict[key]/norm_1 for key in input_dict.keys()}

def updateDict(key, input_dict):
    if not key == 'LOCAL':
        if key in input_dict:
            input_dict[key] = input_dict[key]+1
        else:
            input_dict[key] = 1
    return input_dict

def plotMap(src_loc_count, dst_loc_count):
    # animate = FuncAnimation(fig, updateMap, frames = 100)
    animate = FuncAnimation(fig, updateMap, fargs=(src_loc_count, dst_loc_count), init_func=initMap, frames = 100)
    plt.show()

def initMap():
    for country in shpreader.Reader(countries_shp).records():
        ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(0, 0, 0), label=country.attributes['NAME_LONG'])

def updateMap(data):
    global src_loc_count
    global dst_loc_count

    pkt = scapy.sniff(count = 1, iface = INTERFACE)
    try:
        srcIP = pkt[0].getlayer("IP").src
        dstIP = pkt[0].getlayer("IP").dst

        srcCC = 'LOCAL' if srcIP in LOCAL_IPS else ric.getCountryCodeFromIP(srcIP)
        dstCC = 'LOCAL' if dstIP in LOCAL_IPS else ric.getCountryCodeFromIP(dstIP)

        src_loc_count = normalizeDict(updateDict(srcCC, src_loc_count))
        dst_loc_count = normalizeDict(updateDict(dstCC, dst_loc_count))

        print(srcIP, '\t', srcCC, '\t', dstIP, '\t', dstCC, '\t', datetime.datetime.now())
        
        for country in shpreader.Reader(countries_shp).records():
            if country.attributes['ISO_A2'] in src_loc_count:
                val = src_loc_count[country.attributes['ISO_A2']]
                ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(val, val, val), label=country.attributes['NAME_LONG'])
    
    except Exception as e: 
        print()

def snyf(src_loc_count, dst_loc_count):
    print('Starting Snyfing')
    
    while True:
        pkt = scapy.sniff(count = 1, iface = INTERFACE)
        
        try:
            srcIP = pkt[0].getlayer("IP").src
            dstIP = pkt[0].getlayer("IP").dst

            srcCC = 'LOCAL' if srcIP in LOCAL_IPS else ric.getCountryCodeFromIP(srcIP)
            dstCC = 'LOCAL' if dstIP in LOCAL_IPS else ric.getCountryCodeFromIP(dstIP)

            src_loc_count = normalizeDict(updateDict(srcCC, src_loc_count))
            dst_loc_count = normalizeDict(updateDict(dstCC, dst_loc_count))
            # print(srcIP, dstIP)
            print(srcIP, '\t', srcCC, '\t', dstIP, '\t', dstCC, '\t', datetime.datetime.now())
            # print(1, src_loc_count, dst_loc_count)
            # plotMap(src_loc_count)
            # plotMap(src_loc_count)
        except Exception as e: 
            print(str(e))

def setLocalIP():
    print('Getting local IP')
    IPs = os.popen('ipconfig | findstr "IPv4 Default Gateway"').read().split('\n')[:-1]
    for ip in IPs:
        LOCAL_IPS.append(ip.split(': ')[1])

if __name__=='__main__':
    setLocalIP()
    animate = FuncAnimation(fig, updateMap, init_func=initMap, frames = 100)
    plt.show()
