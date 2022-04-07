import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import itertools

from pytz import country_names

cmap = mpl.cm.Blues

test = 0
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)


ax = plt.axes(projection=ccrs.PlateCarree())

for country in shpreader.Reader(countries_shp).records():
    print(country.attributes['NAME_LONG'], country.attributes['ISO_A2'])
    
    # if len(country.attributes['NAME_LONG']) < 5:    
    #     ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(0, 0, 0), label=country.attributes['NAME_LONG'])
    # else:
    #     ax.add_geometries([country.geometry], ccrs.PlateCarree(), facecolor=(0.588, 0.588, 0.588), label=country.attributes['NAME_LONG'])
    # print(country.attributes['NAME_SORT'], country.attributes['NAME_LONG'], country.attributes['SOV_A3'], )

# print(shpreader.Reader(countries_shp).records())
# plt.show()