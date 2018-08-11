#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 22:05:32 2018

@author: Jessica Tomaszewski
"""

from matplotlib import pyplot as plt
import numpy as np
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
z_wrf = nc_fid.variables['z_wrf'][:]
z_sod = nc_fid.variables['z_sod'][:]
#################################


#################################
# Prep data
hourly_ws_wrf_profile = np.sqrt(hourly_u_wrf_profile**2 + hourly_v_wrf_profile**2)
hourly_ws_sod_profile = np.sqrt(hourly_u_sod_profile**2 + hourly_v_sod_profile**2)

hour = 0 #UTC

if hour < 10:
    hourstring = '0'
else:
    hourstring = ''


# filter winds by total power deficit of interest P in MW
P = 48
power_deficit = total_power_deficit.reshape([31,24])
u_wrf_filter = np.ones([31,24,len(z_wrf)])*np.nan
u_sod_filter = np.ones([31,24,len(z_sod)])*np.nan
v_wrf_filter = np.ones([31,24,len(z_wrf)])*np.nan
v_sod_filter = np.ones([31,24,len(z_sod)])*np.nan
ws_wrf_filter = np.ones([31,24,len(z_wrf)])*np.nan
ws_sod_filter = np.ones([31,24,len(z_sod)])*np.nan

for z in np.arange(len(z_wrf)):
    for d in np.arange(31):
        for h in np.arange(24):
            if power_deficit[d,h] > P:
                u_wrf_filter[d,h,z] = hourly_u_wrf_profile[d,h,z]
                v_wrf_filter[d,h,z] = hourly_v_wrf_profile[d,h,z]
                ws_wrf_filter[d,h,z] = hourly_ws_wrf_profile[d,h,z]

for z in np.arange(len(z_sod)):
    for d in np.arange(31):
        for h in np.arange(24):
            if power_deficit[d,h] > P:
                u_sod_filter[d,h,z] = hourly_u_sod_profile[d,h,z]
                v_sod_filter[d,h,z] = hourly_v_sod_profile[d,h,z]
                ws_sod_filter[d,h,z] = hourly_ws_sod_profile[d,h,z]
 
# Comment this out if not filtering           
u_wrf = u_wrf_filter
v_wrf = v_wrf_filter
ws_wrf = ws_wrf_filter
u_sod = u_sod_filter
v_sod = v_sod_filter
ws_sod = ws_sod_filter

# calculate averages
u_sod_avg = np.ones(len(z_sod))*np.nan
v_sod_avg = np.ones(len(z_sod))*np.nan
ws_sod_avg = np.ones(len(z_sod))*np.nan
u_wrf_avg = np.ones(len(z_wrf))*np.nan
v_wrf_avg = np.ones(len(z_wrf))*np.nan
ws_wrf_avg = np.ones(len(z_wrf))*np.nan

# sodar mean
for z in np.arange(len(z_sod)):
    u_sod_avg[z] = np.nanmean(u_sod[:,:,z])
    v_sod_avg[z] = np.nanmean(v_sod[:,:,z])
    ws_sod_avg[z] = np.nanmean(ws_sod[:,:,z])
# wrf mean
for z in np.arange(len(z_wrf)):
    u_wrf_avg[z] = np.nanmean(u_wrf[:,:,z])
    v_wrf_avg[z] = np.nanmean(v_wrf[:,:,z])
    ws_wrf_avg[z] = np.nanmean(ws_wrf[:,:,z])
#################################


#################################
# Make figure

# font sizes
cb_fs = 18
lb_fs = 16
tk_fs = 13
bx_fs = 19

fig = plt.figure()
ax = plt.subplot(111)

plt.plot(ws_sod_avg, z_sod, lw=1.8, zorder=10)
plt.plot(ws_wrf_avg[2:-1], z_wrf[2:-1], lw=1.8, zorder=10)

plt.barbs(ws_sod_avg, z_sod, u_sod_avg*1.94, v_sod_avg*1.94, zorder=11)
plt.barbs(ws_wrf_avg[2:-1], z_wrf[2:-1], u_wrf_avg[2:-1]*1.94, v_wrf_avg[2:-1]*1.94, zorder=11)

ax.set_xlabel('Wind Speed (m s$^{-1}$)', fontsize=lb_fs)
ax.set_ylabel(r'z (m $AGL$)', fontsize=lb_fs)
plt.tick_params(axis='both', which='major', labelsize=tk_fs)
plt.grid()
plt.xlim(1,9)
plt.ylim(0,160)

plt.text(0.03, 0.91, '      Monthly mean, Power deficit > '+str(P)+' MW', ha='left', fontsize=bx_fs-4, transform=ax.transAxes,
         bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.text(0.03, 0.8, 'Sodar', color='b', ha='left', fontsize=bx_fs, transform=ax.transAxes,
         bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.text(0.03, 0.7, 'WRF', color='g', ha='left', fontsize=bx_fs, transform=ax.transAxes,
         bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.text(0.02, 0.9, '(c)', ha='left', transform=ax.transAxes, fontsize=bx_fs+1)
#################################