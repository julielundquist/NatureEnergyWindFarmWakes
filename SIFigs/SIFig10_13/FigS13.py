#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:46:38 2018

@author: Jessica Tomaszewski
"""


from matplotlib import pyplot as plt
import numpy as np
import netCDF4 as nc4



#################################
# Read NETCDF of simulation data
path = ‘’
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
hourly_wd_wrf_profile = nc_fid.variables['hourly_wd_wrf_profile'][:]
hourly_wd_sod_profile = nc_fid.variables['hourly_wd_sod_profile'][:]
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
    
# organize for plotting
ws_wrf_plt = np.ravel(hourly_ws_wrf_profile[22:25,:,6])
ws_sod_plt = np.ravel(hourly_ws_sod_profile[22:25,:,5])
wd_wrf_plt = np.ravel(hourly_wd_wrf_profile[22:25,:,6])
wd_sod_plt = np.ravel(hourly_wd_sod_profile[22:25,:,5])
u_wrf_plt = np.ravel(hourly_u_wrf_profile[22:25,:,6])
v_wrf_plt = np.ravel(hourly_v_wrf_profile[22:25,:,6])
u_sod_plt = np.ravel(hourly_u_sod_profile[22:25,:,5])
v_sod_plt = np.ravel(hourly_v_sod_profile[22:25,:,5])
#################################


#################################
# Make figure

# font sizes
cb_fs = 18
lb_fs = 16
tk_fs = 13
bx_fs = 19

# x axis
time = np.arange(len(ws_wrf_plt))

# for barbs
barb_line = np.ones(len(time))*-2
bottom_line = np.ones(len(time))*-4
stag=2

fig = plt.figure(figsize=[10,4.5])
ax = plt.subplot(111)

plt.plot(time, ws_sod_plt, lw=1.8, zorder=10)
plt.plot(time, ws_wrf_plt, lw=1.8, zorder=10)

plt.fill_between(time, 0, bottom_line, alpha=0.3, facecolor='gray',lw=0.2)
bb = plt.barbs(time[::stag], barb_line[::stag],
               u_sod_plt[::stag]*1.94, v_sod_plt[::stag]*1.94,
               length=7, color='b', zorder=11)
bb = plt.barbs(time[::stag], barb_line[::stag],
               u_wrf_plt[::stag]*1.94, v_wrf_plt[::stag]*1.94,
               length=7, color='g', zorder=11)
plt.plot(time,barb_line,'k',lw=1)

ax.set_xlabel('Time (UTC)', fontsize=lb_fs)
ax.set_ylabel('           Wind Speed (m s$^{-1}$)', fontsize=lb_fs)
plt.tick_params(axis='both', which='major', labelsize=tk_fs)
plt.grid()
plt.xlim(12,60)
plt.ylim(-4,14)
ax.set_xticks(np.arange(12,61,6))
ax.set_xticklabels(['12','18','00','06','12','18','00','06','12'])
ax.set_yticks(np.arange(0,15,2))

plt.text(0.02, 0.9, 'Sodar', color='b', ha='left', fontsize=bx_fs, transform=ax.transAxes,
         bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))
plt.text(0.02, 0.8, 'WRF', color='g', ha='left', fontsize=bx_fs, transform=ax.transAxes,
         bbox=dict(facecolor='w', edgecolor='none', alpha=0.7))

plt.text(0, -0.12, 'Jan 23', ha='center', transform=ax.transAxes, fontsize=tk_fs)
plt.text(1, -0.12, 'Jan 25', ha='center', transform=ax.transAxes, fontsize=tk_fs)

#plt.savefig('timeseries_compare_v2.pdf', bbox_inches='tight')
#################################