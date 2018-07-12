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

clat = grd.variables["geolat"][:,:]
clon = grd.variables["geolon"][:,:]

file1 = '../per_longshore/prog.nc'
file2 = 'prog_0.nc'
file3 = 'prog_1.nc'
file4 = 'prog.nc'

nc1 = netCDF4.Dataset(file1, "r")
nc2 = netCDF4.Dataset(file2, "r")
nc3 = netCDF4.Dataset(file3, "r")
nc4 = netCDF4.Dataset(file4, "r")
time = nc1.variables["time"][:]
ntim = len(time)
stats = np.zeros((3, ntim))
#   for it in range(10):
fig = plt.figure(figsize=(8,6))
for it in range(ntim):
    ssh1 = nc1.variables["v"][it,:,:,:]
    ssh2 = nc2.variables["v"][it,:,:,:]
    ssh3 = nc3.variables["v"][it,:,:,:]
    ssh4 = nc4.variables["v"][it,:,:,:]
    stats[0,it] = rmse(ssh2, ssh1)
    stats[1,it] = rmse(ssh3, ssh1)
    stats[2,it] = rmse(ssh4, ssh1)


nc1.close()
nc2.close()
nc3.close()

plt.title('v-velocity RMSE')
plt.plot(time, stats[0,:], 'r-.', label = 'Flather')
plt.plot(time, stats[1,:], 'b-.', label = 'Flather, Orlanski')
plt.plot(time, stats[2,:], 'g-.', label = 'Flather, oblique')
plt.legend(loc=1)
fig.savefig('stats_plot.png')
plt.close()

