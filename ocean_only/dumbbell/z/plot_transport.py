import numpy as np
import netCDF4
import os
import sys
import subprocess
import pyroms
from pyroms_toolbox import jday2date
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

grd = netCDF4.Dataset('ocean_geometry.nc', "r")
grd2 = netCDF4.Dataset('../z_sub/ocean_geometry.nc', "r")

clat = grd.variables["geolat"][:,40:80]
clon = grd.variables["geolon"][:,40:80]
clat2 = grd2.variables["geolat"][:]
clon2 = grd2.variables["geolon"][:]

file1 = 'prog.nc'
file2 = '../z_sub_clamp/prog_leak.nc'

nc1 = netCDF4.Dataset(file1, "r")
nc2 = netCDF4.Dataset(file2, "r")
time = nc1.variables["Time"][:]
ntim = len(time)
#ntim = len(time)//8
stats = np.zeros((8, ntim))
#   for it in range(10):
fig = plt.figure(figsize=(8,6))
for it in range(ntim):
    h1 = nc1.variables["h"][it,:,:,40:80]
    h2 = nc2.variables["h"][it,:,:,:]
    u1 = nc1.variables["u"][it,:,:,40:81]
    u2 = nc2.variables["u"][it,:,:,:]
    ssh1 = nc1.variables["SSH"][it,:,40:81]
    ssh2 = nc2.variables["SSH"][it,:,:]
    stats[0,it] = np.sum(h1[:,:,0]*u1[:,:,0])
    stats[1,it] = np.sum(h2[:,:,0]*u2[:,:,0])
    stats[2,it] = np.sum(h1[:,:,-1]*u1[:,:,-1])
    stats[3,it] = np.sum(h2[:,:,-1]*u2[:,:,-1])
    stats[4,it] = np.sum(ssh1[:,1]-ssh1[:,0])
    stats[5,it] = np.sum(ssh2[:,1]-ssh2[:,0])
    stats[6,it] = np.sum(ssh1[:,-1]-ssh1[:,-2])
    stats[7,it] = np.sum(ssh2[:,-1]-ssh2[:,-2])


nc1.close()
nc2.close()

time = time[0:ntim]
plt.title('testing theory')
#plt.plot(time, stats[0,:], 'r-.', label = 'hu1 west')
#plt.plot(time, stats[1,:], 'b-.', label = 'hu2 west')
#plt.plot(time, stats[2,:], 'g-.', label = 'hu1 east')
#plt.plot(time, stats[3,:], 'k-.', label = 'hu2 east')
plt.plot(time, (stats[0,:]-stats[1,:]), 'g--', label = 'hu1 west-east')
plt.plot(time, (stats[2,:]-stats[3,:]), 'k--', label = 'hu2 west-east')
#plt.plot(time, stats[4,:], 'r-', label = 'slope1 west')
#plt.plot(time, stats[5,:], 'b-', label = 'slope2 west')
#plt.plot(time, stats[6,:], 'g-', label = 'slope1 east')
#plt.plot(time, stats[7,:], 'k-', label = 'slope2 east')
plt.legend(loc=1)
fig.savefig('drain_plot.png')
plt.close()

