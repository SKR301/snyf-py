from scapy import all as scapy
import read_ip_csv as ric
import datetime
import os
import sys
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib as mpl

INTERFACE = sys.argv[1]
# INTERFACE = 'Ethernet'
LOCAL_IPS = []
COLORS = [(0,0.10,1),(0,1,1),(0,1,0.53),(0.5,1,0),(1,0.83,0),(1,0.5,0),(1,0,0)]
src_loc_count = {}
dst_loc_count = {}

# initializing plot graph
cmap = mpl.cm.Blues
fig = plt.figure(figsize=(7.5, 5))
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

# update new country_code and count to dict
def updateDict(key, input_dict):
    if not key == 'LOCAL':
        if key in input_dict:
            input_dict[key] = input_dict[key]+1
        else:
            input_dict[key] = 1
    return input_dict

# initialize map plot
def initMap():
    for country in shpreader.Reader(countries_shp).records():
        ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(1, 1, 1), label=country.attributes['NAME_LONG'])

# return color for heat map
def retCol(count):
    val = COLORS[0]
    if count > 10:
        val = COLORS[1]
    if count > 50:
        val = COLORS[2]
    if count > 100:
        val = COLORS[3]
    if count > 500:
        val = COLORS[4]
    if count > 1000:
        val = COLORS[5]
    if count > 5000:
        val = COLORS[6]
    return val

# update for animation
def updateMap(data):
    global src_loc_count
    global dst_loc_count
    global COLORS

    pkt = scapy.sniff(count = 1, iface = INTERFACE)                             # sniff
    try:
        srcIP = pkt[0].getlayer("IP").src
        dstIP = pkt[0].getlayer("IP").dst

        srcCC = 'LOCAL' if srcIP in LOCAL_IPS else ric.getCountryCodeFromIP(srcIP)
        dstCC = 'LOCAL' if dstIP in LOCAL_IPS else ric.getCountryCodeFromIP(dstIP)

        # src_loc_count = normalizeDict(updateDict(srcCC, src_loc_count))       # plot just source IP graph
        # dst_loc_count = normalizeDict(updateDict(dstCC, dst_loc_count))       # plot just destinatioo+n IP graph
        src_loc_count = updateDict(srcCC, src_loc_count)                        # plot both IP graph
        src_loc_count = updateDict(dstCC, dst_loc_count)                        # plot both IP graph

        print(srcIP, '\t', srcCC, '\t', dstIP, '\t', dstCC, '\t', datetime.datetime.now())
        
        for country in shpreader.Reader(countries_shp).records():
            if country.attributes['ISO_A2'] in src_loc_count:
                val = retCol(src_loc_count[country.attributes['ISO_A2']])
                ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=val, label=country.attributes['NAME_LONG'])
    
    except Exception as e: 
        print()

# check LOCAL IP
def setLocalIP():
    print('Getting local IP')
    IPs = os.popen('ipconfig | findstr "IPv4 Default Gateway"').read().split('\n')[:-1]
    for ip in IPs:
        LOCAL_IPS.append(ip.split(': ')[1])

if __name__=='__main__':
    setLocalIP()
    animate = FuncAnimation(fig, updateMap, init_func=initMap, frames = 100)
    plt.show()
