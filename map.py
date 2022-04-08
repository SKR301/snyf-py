import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib as mpl

cmap = mpl.cm.Blues
fig = plt.figure(figsize=(7.5, 5))

test = 0
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)


val = 0
ax = plt.axes(projection=ccrs.PlateCarree())
geometry = ''
for country in shpreader.Reader(countries_shp).records():
    # print(country.attributes['NAME_LONG'], country.attributes['ISO_A2'])
    
    if country.attributes['ISO_A2'] == 'IN':    
        geometry = ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(val, val, val), label=country.attributes['NAME_LONG'])
    else:
        geometry = ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(val, val, val), label=country.attributes['NAME_LONG'])

def update_map(data):
    val = (data%255)/255
    print(val)
    for country in shpreader.Reader(countries_shp).records():
        if country.attributes['ISO_A2'] == 'IN':    
            ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(val, val, val), label=country.attributes['NAME_LONG'])

# print(country.geometry)
animatedPlt = FuncAnimation(fig, update_map, frames = 100)
plt.show()
