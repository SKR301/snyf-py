from scapy import all as scapy
import read_ip_csv as ric
import datetime
import os
import threading
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

cmap = mpl.cm.Blues
fig = plt.figure(figsize=(7.5, 5))

shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
ax = plt.axes(projection=ccrs.PlateCarree())

def plotMap(src_loc_count, dst_loc_count):
    animate = FuncAnimation(fig, updateMap, fargs=(src_loc_count, dst_loc_count), init_func=initMap, frames = 100)
    plt.show()

def initMap():
    for country in shpreader.Reader(countries_shp).records():
        ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(0, 0, 0), label=country.attributes['NAME_LONG'])

def updateMap(data, src_loc_count, dst_loc_count):
    global val
    for country in shpreader.Reader(countries_shp).records():
        if country.attributes['ISO_A2'] in src_loc_count:
            val = src_loc_count[country.attributes['ISO_A2']]
            ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(val, val, val), label=country.attributes['NAME_LONG'])
        else:
            print(src_loc_count)

def snyf(src_loc_count, dst_loc_count):
    # global src_loc_count
    # global dst_loc_count
    
    while True:
        pkt = scapy.sniff(count =1, iface = INTERFACE)
        
        try:
            srcIP = pkt[0].getlayer("IP").src
            dstIP = pkt[0].getlayer("IP").dst

            srcCC = 'LOCAL' if srcIP in LOCAL_IPS else ric.getCountryCodeFromIP(srcIP)
            dstCC = 'LOCAL' if dstIP in LOCAL_IPS else ric.getCountryCodeFromIP(dstIP)

            src_loc_count = normalizeDict(updateDict(srcCC, src_loc_count))
            dst_loc_count = normalizeDict(updateDict(dstCC, dst_loc_count))
            
            # print(srcIP, '\t', srcCC, '\t', dstIP, '\t', dstCC, '\t', datetime.datetime.now())
            # print(src_loc_count, dst_loc_count)
            print('1',src_loc_count)
            # plotMap(src_loc_count)
            # plotMap(src_loc_count)
        except Exception as e: 
            print()

def setLocalIP():
    IPs = os.popen('ipconfig | findstr IPv4').read().split('\n')[:-1]
    for ip in IPs:
        LOCAL_IPS.append(ip.split(': ')[1])
        
if __name__=='__main__':
    setLocalIP()

    manager = multiprocessing.Manager()
    src_loc_count = manager.dict()
    dst_loc_count = manager.dict()
    p1 = multiprocessing.Process(target=snyf, args=(src_loc_count,dst_loc_count,))
    p2 = multiprocessing.Process(target=plotMap, args=(src_loc_count,dst_loc_count,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()