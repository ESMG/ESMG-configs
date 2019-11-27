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

file1 = '../per_crossshore/prog.nc'
file2 = 'prog_6.nc'
file3 = 'prog_7.nc'
file4 = 'prog_8.nc'
file5 = 'prog_9.nc'
file6 = 'prog_1.nc'
file7 = 'prog_2.nc'
file8 = 'prog_3.nc'

nc1 = netCDF4.Dataset(file1, "r")
nc2 = netCDF4.Dataset(file2, "r")
nc3 = netCDF4.Dataset(file3, "r")
nc4 = netCDF4.Dataset(file4, "r")
nc5 = netCDF4.Dataset(file5, "r")
nc6 = netCDF4.Dataset(file6, "r")
nc7 = netCDF4.Dataset(file7, "r")
nc8 = netCDF4.Dataset(file8, "r")
time = nc1.variables["time"][:]
ntim = len(time)//6
stats = np.zeros((7, ntim))
#   for it in range(10):
fig = plt.figure(figsize=(8,6))
for it in range(ntim):
    ssh1 = nc1.variables["v"][it,:,:,:]
    ssh2 = nc2.variables["v"][it,:,:,:]
    ssh3 = nc3.variables["v"][it,:,:,:]
    ssh4 = nc4.variables["v"][it,:,:,:]
    ssh5 = nc5.variables["v"][it,:,:,:]
    ssh6 = nc6.variables["v"][it,:,:,:]
    ssh7 = nc7.variables["v"][it,:,:,:]
    ssh8 = nc8.variables["v"][it,:,:,:]
    stats[0,it] = rmse(ssh2, ssh1)
    stats[1,it] = rmse(ssh3, ssh1)
    stats[2,it] = rmse(ssh4, ssh1)
    stats[3,it] = rmse(ssh5, ssh1)
    stats[4,it] = rmse(ssh6, ssh1)
    stats[5,it] = rmse(ssh7, ssh1)
    stats[6,it] = rmse(ssh8, ssh1)


nc1.close()
nc2.close()
nc3.close()
nc4.close()
nc5.close()
nc6.close()
nc7.close()
nc8.close()

plt.title('v-velocity RMSE')
plt.plot(time[:ntim], stats[0,:], 'r-.', label = 'Flather')
plt.plot(time[:ntim], stats[1,:], 'b-.', label = 'Flather, Orlanski')
plt.plot(time[:ntim], stats[2,:], 'g-.', label = 'Flather, oblique')
plt.plot(time[:ntim], stats[3,:], 'k--', label = 'C., Flather, Marsch')
plt.plot(time[:ntim], stats[4,:], 'g--', label = 'C., Flather, oblique')
plt.plot(time[:ntim], stats[5,:], 'b--', label = 'C., Flather, Orlanski')
plt.plot(time[:ntim], stats[6,:], 'r--', label = 'C., Flather')
plt.legend(loc=1)
fig.savefig('stats_plot.png')
plt.close()

