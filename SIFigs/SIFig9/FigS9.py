#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 22:27:50 2017

@author: Jessica Tomaszewski
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns




# font sizes
cb_fs = 18
lb_fs = 22
tk_fs = 14
bx_fs = 20


colors = sns.color_palette('Set2',8)
colors2 = sns.color_palette('muted',8)

wspd = np.arange(1,26)
power = np.array([-2453.3799,7151.7,36637.9573,88832.3592,170460.237,294580.8897,467812.559,698341.6161,
         956504.6234,1204263.931,1446612.136,1496531.585,1493823.132,1491935.253,1490804.657,
         1489572.239,1488430.314,1486917.827,1486352.999,1485646.336,1483952.837,1482943.889,
         1482753.694,1479162.15,1478506.099])/1e6
   
thrust = np.array([np.nan,np.nan,0.9039,0.7498,0.7195,0.7196,0.7197,0.7198,0.6725,0.5945,0.5229,
                   0.3739,0.2833,0.2227,0.1794,0.1473,0.1228,0.1037,0.0887,0.0765,0.0666,0.0585,
                   0.0517,0.0459,0.041])
 
fig = plt.figure(figsize=[7.7,7])
ax = fig.add_subplot(111)

plt.plot(wspd,power,color='#7570b3',lw=3) 
plt.plot(wspd,thrust,color=colors2[4],lw=3)

plt.tick_params(axis='both', which='major', labelsize=tk_fs)
plt.xlabel('Wind Speed (m s$^{-1}$)', size=lb_fs-6)
plt.xlim(0,24)
plt.ylim(0,1.8)
plt.xticks(np.arange(0,25,3))
plt.yticks(np.arange(0,2,0.3))
plt.grid()

#plt.text(0.05,0.95, '(a)', ha='center', va='center', transform=ax.transAxes, fontsize=lb_fs+4)

plt.text(0.98,0.95, 'Power (MW)', color='#7570b3', ha='right', va='center', transform=ax.transAxes, fontsize=lb_fs)
plt.text(0.98,0.89, 'Thrust Coefficient', color=colors2[4], ha='right', va='center', transform=ax.transAxes, fontsize=lb_fs)
