#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:04:37 2017

@author: Jessica Tomaszewski
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle


path = '' 

#nc_f4 = 'wrfout_d04_2012-12-31_00:00:00'  # Innermost filename
nc_f3 = 'wrfout_d03_2012-12-31_12:00:00'  # Innermost filename
nc_f2 = 'wrfout_d02_2012-12-31_12:00:00'  # Middle filename
nc_f1 = 'wrfout_d01_2012-12-31_12:00:00'  # Outer filename

nc_fid = Dataset(path+nc_f1, 'r')  

# Extract data from NetCDF file
lat1 = nc_fid.variables['XLAT'][:]            # dimensions: (Time, south_north, west_east)
lon1 = nc_fid.variables['XLONG'][:]           # dimensions: (Time, south_north, west_east)

lllon1 = lon1[0,0,0]
lllat1 = lat1.min()
urlon1 = lon1.max()
urlat1 = lat1.max()-2

nc_fid = Dataset(path+nc_f2, 'r')  

# Extract data from NetCDF file
lat2 = nc_fid.variables['XLAT'][:]            # dimensions: (Time, south_north, west_east)
lon2 = nc_fid.variables['XLONG'][:]           # dimensions: (Time, south_north, west_east)

lllon2 = lon2[0,:,:].min()
lllat2 = lat2[0,:,:].min()
urlon2 = lon2[0,:,:].max()
urlat2 = lat2[0,:,:].max()

nc_fid = Dataset(path+nc_f3, 'r')  

# Extract data from NetCDF file
lat3 = nc_fid.variables['XLAT'][:]            # dimensions: (Time, south_north, west_east)
lon3 = nc_fid.variables['XLONG'][:]           # dimensions: (Time, south_north, west_east)

lllon3 = lon3.min()
lllat3 = lat3.min()
urlon3 = lon3.max()
urlat3 = lat3.max()

fig = plt.figure(figsize=[8,7])
ax = fig.add_subplot(111)

m = Basemap(projection='lcc', lat_0=(lllat1+urlat1)/2., lon_0=(lllon1+urlon1)/2.,
    resolution = 'h', area_thresh = 500, epsg = 32039,
    llcrnrlon=lllon1, llcrnrlat=lllat1,  
    urcrnrlon=urlon1, urcrnrlat=urlat1)

m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Physical_Map', verbose=False, alpha=0.5, zorder=0)

# plot 1km
x0,y0 = m(-100.62, 32.454564)
s = m.plot(x0, y0, 's', c='darkred', ms=7, zorder=10)

rect = Rectangle([8e3, 8e3], 2e8, 2e8, ec='none', fc='w', alpha=0.3)
ax.add_artist(rect)

# make a square
lats = [lat2[0,:,:].min(), lat2[0,:,:].max(), lat2[0,:,:].max(), lat2[0,:,:].min()]
lons = [lon2[0,0,:].min(), lon2[0,:,:].min(), lon2[0,:,:].max(), lon2[0,0,:].max()]
x, y = m(lons, lats)
xy = zip(x,y)
poly = Polygon(xy, edgecolor='k', facecolor='none', linewidth=1.9, zorder=10)
plt.gca().add_patch(poly)

# make a square
lats = [lat3[0,:,:].min(), lat3[0,:,:].max(), lat3[0,:,:].max(), lat3[0,:,:].min()]
lons = [lon3[0,0,:].min(), lon3[0,:,:].min(), lon3[0,:,:].max(), lon3[0,0,:].max()]
x, y = m(lons, lats)
xy = zip(x,y)
poly = Polygon(xy, edgecolor='k', facecolor='none', linewidth=1.9, zorder=10)
plt.gca().add_patch(poly)

plt.text(236000,3500000,'D01', ha='center', va='center', fontsize=20)
plt.text(1970000,2030000,'D02', ha='center', va='center', fontsize=20)
plt.text(2400000,1240000,'D03', ha='center', va='center', fontsize=16)
plt.text(2680000,1490000,'D04', ha='center', va='center', fontsize=13)

parallels = np.arange(int(lllat1)-10,int(urlat1)+10,4)
m.drawparallels(parallels,labels=[1,0,0,0])
meridians = np.arange(int(lllon1)-10,int(urlon1)+10,6)
m.drawmeridians(meridians,labels=[0,0,0,1])
    
m.drawcoastlines()
m.drawcountries()
m.drawmapboundary()
m.drawstates()
m.drawmapboundary(color='k', linewidth=1.5)