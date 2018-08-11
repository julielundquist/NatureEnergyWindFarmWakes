#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 00:15:28 2018

@author: Jessica Tomaszewski
"""

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4


#################################
# Read NETCDF of simulation data
path = ''
f = 'SI_WRF_sodar_validation.nc'
nc_fid = nc4.Dataset(path+f, 'r')  
#################################


#################################
# Extract variables
total_power_deficit = nc_fid.variables['total_power_deficit'][:]
hourly_u_wrf_profile = nc_fid.variables['hourly_u_wrf_profile'][:]
hourly_v_wrf_profile = nc_fid.variables['hourly_v_wrf_profile'][:]
hourly_u_sod_profile = nc_fid.variables['hourly_u_sod_profile'][:]
hourly_v_sod_profile = nc_fid.variables['hourly_v_sod_profile'][:]
hourly_wd_sod_profile = nc_fid.variables['hourly_wd_sod_profile'][:]
hourly_u_wrf_80m = nc_fid.variables['hourly_u_wrf'][:]
hourly_v_wrf_80m = nc_fid.variables['hourly_v_wrf'][:]
hourly_wd_wrf_80m = nc_fid.variables['hourly_wd_wrf'][:]
z_wrf = nc_fid.variables['z_wrf'][:]
z_sod = nc_fid.variables['z_sod'][:]
#################################


#################################
# Make figure

hourly_ws_wrf_80m = np.sqrt(hourly_u_wrf_80m**2 + hourly_v_wrf_80m**2)
hourly_ws_sod_profile = np.sqrt(hourly_u_sod_profile**2 + hourly_v_sod_profile**2)

all_WS = np.ravel(hourly_ws_wrf_80m)
all_WD = np.ravel(hourly_wd_wrf_80m)

indices = np.logical_not(np.logical_or(np.isnan(all_WS), np.isnan(all_WD)))
WS = all_WS[indices]
WD = all_WD[indices]

ws_80 = np.ravel(hourly_ws_sod_profile[:,:,5])[indices]
wd_80 = np.ravel(hourly_wd_sod_profile[:,:,5])[indices]

indices = np.logical_not(np.logical_or(np.isnan(ws_80), np.isnan(wd_80)))
WS = WS[indices]
WD = WD[indices]

ws_80 = ws_80[indices]
wd_80 = wd_80[indices]

xx = np.arange(len(WD))
for x in xx:
    if WD[x] > 270 and wd_80[x] < 150:
        WD[x] -= 360
    if WD[x] < 100 and wd_80[x] > 200:
        wd_80[x] -= 360

di = ws_80-WS
rmse_WS = np.sqrt(np.nanmean(di**2))
ae_WS = np.nanmean(np.abs(di))

d = wd_80-WD
rmse_WD = np.sqrt(np.nanmean(d**2))
ae_WD = np.nanmean(np.abs(d))

WD[WD<0] = np.nan
wd_80[wd_80<0] = np.nan
#################################


#################################
# Make figure

# font sizes
lb_fs = 15
tk_fs = 13
bx_fs = 17

fig = plt.figure(figsize=[10,4.2])

# ws, 80m
ax = fig.add_subplot(121)
ax.scatter(WS, ws_80, c='b', s=30, alpha=0.3, clip_on = False)
ax.plot(np.linspace(0,30,100), np.linspace(0,30,100), 'k-')
# best fit
WS = WS[:,np.newaxis]
a, resid, _, _ = np.linalg.lstsq(WS, ws_80)
ax.plot(WS, a*WS, 'r-')
plt.xlim(0,20)
plt.ylim(0,20)
plt.xlabel(r'WRF wind speed (m s$^{-1}$)', fontsize=lb_fs)
plt.ylabel(r'Sodar wind speed (m s$^{-1}$)', fontsize=lb_fs)
plt.text(0.02, 0.93, '(a)', ha='left', va='center', transform=ax.transAxes, fontsize=bx_fs+1)
plt.text(0.03, 0.83, 'RMSE = '+ str(np.round(rmse_WS,1)), ha='left', va='center',
         transform=ax.transAxes, fontsize=tk_fs, bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.text(0.03, 0.76, 'MAE = '+ str(np.round(ae_WS,1)), ha='left', va='center',
         transform=ax.transAxes, fontsize=tk_fs, bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.grid()

# wd, 80m
ax = fig.add_subplot(122)
ax.scatter(WD, wd_80, c='b', s=30, alpha=0.3, clip_on = False)
ax.plot(np.linspace(0,360,100), np.linspace(0,360,100), 'k-')
# best fit
indices = np.logical_not(np.logical_or(np.isnan(WD), np.isnan(wd_80)))
WD = WD[indices]
wd_80 = wd_80[indices]
WD = WD[:,np.newaxis]
a, resid, _, _ = np.linalg.lstsq(WD, wd_80)
ax.plot(WD, a*WD, 'r-')
plt.xlim(0,360)
plt.ylim(0,360)
plt.xticks(np.arange(0,370,60))
plt.yticks(np.arange(0,370,60))
plt.xlabel(r'WRF wind direction ($\circ$)', fontsize=lb_fs)
plt.ylabel(r'Sodar wind direction ($\circ$)', fontsize=lb_fs)
plt.text(0.02, 0.93, '(b)', ha='left', va='center', transform=ax.transAxes, fontsize=bx_fs+1)
plt.text(0.03, 0.83, 'RMSE = '+ str(np.round(rmse_WD,1)), ha='left', va='center',
         transform=ax.transAxes, fontsize=tk_fs, bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.text(0.03, 0.76, 'MAE = '+ str(np.round(ae_WD,1)), ha='left', va='center',
         transform=ax.transAxes, fontsize=tk_fs, bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.grid()

#plt.savefig('error_scatter.pdf', bbox_inches='tight')
#################################