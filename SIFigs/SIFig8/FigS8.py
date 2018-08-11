#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 15:29:51 2017

@author: Jessica Tomaszewski
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



Z12 = np.array([   0.        ,   12.80144691,   25.68107224,   38.60124969,
         51.5532608,   64.45528412,   77.37751007,   90.31964874,
        103.20857239,  116.11598969,  129.04255676,  141.98823547,  154.8782959 ,  167.78695679,
        180.71182251,  193.65362549,  206.53762817,  219.43803406,
        232.35481262,  245.28707886, 258.2355957 ,  271.49987793,  284.70544434,  297.25027466,
        309.80990601,  335.72543335,  362.91433716,  393.35961914, 429.29302979,  472.67434692])
        
        
fig = plt.figure(figsize=[6,6.85])
ax = fig.add_subplot(111)

plt.scatter(np.zeros(len(Z12)),Z12,c='g',marker='_',s=25000,lw=1.4)

ax.set_xticklabels(['','','','',''])
plt.ylim(0,200)
plt.xlim(-1,1)
plt.ylabel('Vertical levels in WRF WFP (m)',fontsize=20)
plt.grid()

im = mpimg.imread('turbine.png')

newax = fig.add_axes([0.35, 0.124, 0.4, 0.48], anchor='S', zorder=1, rasterized=False)
newax.imshow(im)
newax.axis('off')