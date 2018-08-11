#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 15:54:15 2018

@author: Jessica Tomaszewski
"""

import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.cm as cm



# font sizes
cb_fs = 18
lb_fs = 18
tk_fs = 14
bx_fs = 20

station = 'San-Angelo'
#station = 'Abilene'

datafile = open(''+station+'_2013_ASOS.txt', 'r')
datafile_b = open(''+station+'_Jan2013_ASOS.txt', 'r')

data = datafile.readlines()[1:]
data = np.array([x.split(',') for x in data])
wspd = np.array(data[:,3]).astype(np.float) * 0.514444
wdir = np.array(data[:,2]).astype(np.float)
wspd[wspd == 'nan'] = np.nan
wdir[wdir == 'nan'] = np.nan
wspd[wspd == 0] = np.nan
wdir[wspd == 0] = np.nan
indices = np.logical_not(np.logical_or(np.isnan(wspd), np.isnan(wdir)))
WS = wspd[indices]
WD = wdir[indices]

data = datafile_b.readlines()[1:]
data = np.array([x.split(',') for x in data])
wspd_b = np.array(data[:,3]).astype(np.float) * 0.514444
wdir_b = np.array(data[:,2]).astype(np.float)
wspd_b[wspd_b == 'nan'] = np.nan
wdir_b[wdir_b == 'nan'] = np.nan
wspd_b[wspd_b == 0] = np.nan
wdir_b[wspd_b == 0] = np.nan
indices = np.logical_not(np.logical_or(np.isnan(wspd_b), np.isnan(wdir_b)))
WS_b = wspd_b[indices]
WD_b = wdir_b[indices]


fig = plt.figure(figsize=[14,6])
rect = [0,0,0.5,1] 
ax = WindroseAxes(fig, rect)
fig.add_axes(ax)

#ax = WindroseAxes.from_ax()
ax.bar(WD, WS, cmap=cm.viridis, normed=True, nsector=36, bins=np.arange(0,14,2)) #summer
plt.text(-0.06, 1, '(a)', ha='left', va='center', transform=ax.transAxes, fontsize=bx_fs+3)
plt.tick_params(axis='x', which='major', labelsize=tk_fs+3)

ax.set_rlabel_position(340) #122, 344, 198, 340
ax.set_rmax(10) #8, 10
ax.set_rticks(np.arange(0,11,2)) 
ax.set_yticklabels(['','  2%','  4%','  6%','  8%','  10%'], fontsize=tk_fs)
#ax.set_yticklabels(['','2%','4%','6%','8%','10%'], fontsize=tk_fs)


rect = [0.52,0,0.5,1] 
ax = WindroseAxes(fig, rect)
fig.add_axes(ax)

ax.bar(WD_b, WS_b, cmap=cm.viridis, normed=True, nsector=36, bins=np.arange(0,14,2)) #summer
plt.text(-0.06, 1, '(b)', ha='left', va='center', transform=ax.transAxes, fontsize=bx_fs+3)
plt.tick_params(axis='x', which='major', labelsize=tk_fs+3)

ax.set_rlabel_position(340) #122, 344, 198, 340
ax.set_rmax(10) #8, 10
ax.set_rticks(np.arange(0,11,2)) 
ax.set_yticklabels(['','  2%','  4%','  6%','  8%','  10%'], fontsize=tk_fs)
#ax.set_yticklabels(['','2%','4%','6%','8%','10%'], fontsize=tk_fs)

# 0.69, 0.13  0.053, 0.14
plt.text(1.13, 0.36, r'Wind Speed (m s$^{-1}$)', ha='center', va='bottom', transform=ax.transAxes,
         rotation=90, fontsize=tk_fs, bbox=dict(facecolor='w', edgecolor='none', alpha=0.8))

#leg = plt.legend(bbox_to_anchor=(0.063, -0.035))
leg = plt.legend(bbox_to_anchor=(1.15, 0.35))
leg.get_texts()[0].set_text('0 - 2')
leg.get_texts()[1].set_text('2 - 4')
leg.get_texts()[2].set_text('4 - 6')
leg.get_texts()[3].set_text('6 - 8')
leg.get_texts()[4].set_text('8 - 10')
leg.get_texts()[5].set_text('10 - 12')
leg.get_texts()[6].set_text('12 +')