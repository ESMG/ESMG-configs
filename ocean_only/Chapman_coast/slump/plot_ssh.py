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
lst = subprocess.getoutput('ls ../tall_slump/prog.nc')
lst = lst.split()
lst_file = lst_file + lst

#grd = pyroms_toolbox.BGrid_GFDL.get_nc_BGrid_GFDL('prog.nc')
grd = netCDF4.Dataset('ocean_geometry.nc', "r")

clat = grd.variables["geolat"][:]
clon = grd.variables["geolon"][:]

#m = Basemap(llcrnrlon=-165.5, llcrnrlat=70.3, urcrnrlon=-128.0, urcrnrlat=71.0,\
#            rsphere=(6378137.00,6356752.3142),\
#            resolution='h', projection='lcc',\
#            lat_0=65., lat_1=70.0, lon_0=-162.)
#x, y = m(clon, clat)
#levels = np.arange(-0.0015, .0015, 0.00005)
levels = [-.005, -.0025, -.00125, -.000625, -.0003125, -.00015625, -7.8125e-05, \
      -3.90625e-05, -1.953125e-05, -9.765625e-06, -4.8828125e-06, -2.44140625e-06, -1.220703125e-06, 0, \
      1.220703125e-06, 2.44140625e-06, 4.8828125e-06, 9.765625e-06, 1.953125e-05, 3.90625e-05, \
	   7.8125e-05, .00015625, .0003125, .000625, .00125, .0025, .005]
cmap = plt.cm.get_cmap("PRGn")

for file in lst_file:
    print("Plotting "+file)
#   m.drawmapboundary(fill_color='0.3')
#   m.drawcoastlines()
    nc = netCDF4.Dataset(file, "r")
    nc2 = netCDF4.Dataset("prog_0.nc", "r")
    nc3 = netCDF4.Dataset("prog_1.nc", "r")
    nc4 = netCDF4.Dataset("prog.nc", "r")
    time = nc.variables["time"][:]
    ntim = len(time)
#   for it in range(10):
#   for it in range(0,ntim,5):
    for it in range(0,ntim):
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(131)
        ax.set_aspect('equal')
        ssh = nc.variables["e"][it,0,165:195,:]
        time = nc.variables["time"][it]
#       cs = m.contourf(x, y, ssh, levels=levels, cmap=cmap)
#       csa = m.contour(x, y, ssh, levels=levels, linewidths=(0.5,))
        plt.title('Flather')

        ssh2 = nc2.variables["e"][it,0,:,:]
        cs2 = plt.contourf(clon, clat, ssh2-ssh, levels=levels, cmap=cmap, extend='both')
        csa = plt.contour(clon, clat, ssh2-ssh, levels=levels, linewidths=(0.5,))

        ax2 = fig.add_subplot(132)
        ax2.set_aspect('equal')
        plt.title('Orlanski')
        ssh3 = nc3.variables["e"][it,0,:,:]
        cs3 = plt.contourf(clon, clat, ssh3-ssh, levels=levels, cmap=cmap, extend='both')
        csa = plt.contour(clon, clat, ssh3-ssh, levels=levels, linewidths=(0.5,))

        ax3 = fig.add_subplot(133)
        ax3.set_aspect('equal')
        plt.title('Oblique')
        ssh4 = nc4.variables["e"][it,0,:,:]
        cs4 = plt.contourf(clon, clat, ssh4-ssh, levels=levels, cmap=cmap, extend='both')
        csa = plt.contour(clon, clat, ssh4-ssh, levels=levels, linewidths=(0.5,))

        cbaxes = fig.add_axes([0.1, 0.05, 0.8, 0.03])
        plt.colorbar(orientation='horizontal', cax=cbaxes)

        print('printing frame:', it)
        fig.savefig('movie/ssh_%(number)04d.png'%{'number': it})
        plt.close()

    nc.close()

