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
file2 = '../z_sub/prog_big_nud_or.nc'
file3 = '../z_sub/prog_big_nud_ob.nc'
file4 = '../z_sub/prog_big_vort.nc'
file5 = '../z_sub/prog_big_nonud_or.nc'
file6 = '../z_sub/prog_big_nonud_ob.nc'
#file7 = '../z_sub/prog_oldob_nonud.nc'

nc1 = netCDF4.Dataset(file1, "r")
nc2 = netCDF4.Dataset(file2, "r")
nc3 = netCDF4.Dataset(file3, "r")
nc4 = netCDF4.Dataset(file4, "r")
nc5 = netCDF4.Dataset(file5, "r")
nc6 = netCDF4.Dataset(file6, "r")
#nc7 = netCDF4.Dataset(file7, "r")
time = nc1.variables["Time"][:]
ntim = len(time)
stats = np.zeros((6, ntim))
#   for it in range(10):
fig = plt.figure(figsize=(8,6))
for it in range(ntim):
    ssh1 = nc1.variables["salt"][it,:,:,40:80]
    ssh2 = nc2.variables["salt"][it,:,:,:]
    ssh3 = nc3.variables["salt"][it,:,:,:]
    ssh4 = nc4.variables["salt"][it,:,:,:]
    ssh5 = nc5.variables["salt"][it,:,:,:]
    ssh6 = nc6.variables["salt"][it,:,:,:]
#   ssh7 = nc7.variables["salt"][it,:,:,:]
    stats[0,it] = rmse(ssh2, ssh1)
    stats[1,it] = rmse(ssh3, ssh1)
    stats[2,it] = rmse(ssh4, ssh1)
    stats[3,it] = rmse(ssh5, ssh1)
    stats[4,it] = rmse(ssh6, ssh1)
#   stats[5,it] = rmse(ssh7, ssh1)


nc1.close()
nc2.close()
nc3.close()
nc4.close()
nc5.close()
#c6.close()
#nc7.close()

plt.title('Salinity RMSE')
plt.plot(time, stats[0,:], 'r-.', label = 'orlanski+nud')
plt.plot(time, stats[1,:], 'b-.', label = 'oblique+nud')
plt.plot(time, stats[2,:], 'g-.', label = 'orlanski+nud+vort')
plt.plot(time, stats[3,:], 'r-', label = 'orlanski')
plt.plot(time, stats[4,:], 'b-', label = 'oblique')
#lt.plot(time, stats[5,:], 'g-', label = 'old_oblique')
plt.legend(loc=1)
fig.savefig('stats_plot.png')
plt.close()

