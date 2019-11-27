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


# draw line around map projection limb.
# color background of map projection region.
# missing values over land will show up this color.
# plot sst, then ice with pcolor
# add a title.
#year = int(sys.argv[1])
#lst_year = [year]

lst_file = []

#for year in lst_year:
#    year = np.str(year)
#lst = subprocess.getoutput('ls clima/*.nc')
lst = subprocess.getoutput('ls prog_half.nc')
lst = lst.split()
lst_file = lst_file + lst

#grd = pyroms_toolbox.BGrid_GFDL.get_nc_BGrid_GFDL('prog.nc')
grd = netCDF4.Dataset('ocean_geometry.nc', "r")

clat = grd.variables["geolat"][:]
clon = grd.variables["geolon"][:]

#levels = np.arange(-2.8, 2.8, 0.05)
levels = np.arange(-.05, .05, 0.005)
#levels = [-.158, -.126, -.1, -.079, -.063, -.050, -.040, -.032, -.025, -.020, -.016, -.013, -.01, -.008, 0, \
#           .008, .01, .013, .016, .020, .025, .032, .04, .05, .063, .079, .1, .126, .158]
cmap = plt.cm.get_cmap("PRGn")

for file in lst_file:
    print("Plotting "+file)
#   m.drawmapboundary(fill_color='0.3')
#   m.drawcoastlines()
    nc = netCDF4.Dataset(file, "r")
    time = nc.variables["Time"][:]
    ntim = len(time)
    for it in range(0,ntim):
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ssh = nc.variables["e"][it,0,:,:]
        time = nc.variables["Time"][it]
#       cs = m.contourf(x, y, ssh, levels=levels, cmap=cmap)
#       csa = m.contour(x, y, ssh, levels=levels, linewidths=(0.5,))
        cs = plt.contourf(clon, clat, ssh, levels=levels, cmap=cmap, extend='both')
#       plt.plot([-100,-100], [-50,50], 'b-')
#       plt.plot([100,100], [-50,50], 'b-')
        plt.title('Sea Level Height (m)')

        cbaxes = fig.add_axes([0.1, 0.05, 0.8, 0.03])
        plt.colorbar(orientation='horizontal', cax=cbaxes)

        print('printing frame:', it)
        fig.savefig('movie/ssh_%(number)04d.png'%{'number': it})
        plt.close()

    nc.close()

