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
lst = subprocess.getoutput('ls prog.nc')
lst = lst.split()
lst_file = lst_file + lst

#grd = pyroms_toolbox.BGrid_GFDL.get_nc_BGrid_GFDL('prog.nc')
grd = netCDF4.Dataset('ocean_geometry.nc', "r")
grd2 = netCDF4.Dataset('../z_sub/ocean_geometry.nc', "r")

clat = grd.variables["geolatb"][:]
clon = grd.variables["geolonb"][:]
clat2 = grd2.variables["geolatb"][:]
clon2 = grd2.variables["geolonb"][:]

#m = Basemap(llcrnrlon=-165.5, llcrnrlat=70.3, urcrnrlon=-128.0, urcrnrlat=71.0,\
#            rsphere=(6378137.00,6356752.3142),\
#            resolution='h', projection='lcc',\
#            lat_0=65., lat_1=70.0, lon_0=-162.)
#x, y = m(clon, clat)
levels = np.arange(-.00028, .00028, 0.000002)
cmap = plt.cm.get_cmap("seismic")

for file in lst_file:
    print("Plotting "+file)
#   m.drawmapboundary(fill_color='0.3')
#   m.drawcoastlines()
    nc = netCDF4.Dataset(file, "r")
    nc2 = netCDF4.Dataset("../z_sub/prog_big_nud_or.nc", "r")
    nc3 = netCDF4.Dataset("../z_sub/prog_big_best.nc", "r")
    time = nc.variables["Time"][:]
    ntim = len(time)
#   for it in range(10):
    for it in range(0,ntim,40):
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(311)
        ax.set_aspect('equal')
        ax.axis(xmin=-300,xmax=300)
        ssh = nc.variables["RV"][it,0,:,:]
        time = nc.variables["Time"][it]
#       cs = m.contourf(x, y, ssh, levels=levels, cmap=cmap)
#       csa = m.contour(x, y, ssh, levels=levels, linewidths=(0.5,))
        cs = plt.contourf(clon, clat, ssh, levels=levels, cmap=cmap, extend='both')
        plt.plot([-100,-100], [-100,100], 'b-')
        plt.plot([100,100], [-100,100], 'b-')
        plt.title('Surface RV')
#       csa = plt.contour(clon, clat, ssh, levels=levels, linewidths=(0.5,))

        ax2 = fig.add_subplot(312)
        ax2.set_aspect('equal')
        ax2.axis(xmin=-300,xmax=300)
        ssh2 = nc2.variables["RV"][it,0,:,:]
        cs2 = plt.contourf(clon2, clat2, ssh2, levels=levels, cmap=cmap, extend='both')

        ax3 = fig.add_subplot(313)
        ax3.set_aspect('equal')
        ax3.axis(xmin=-300,xmax=300)
        ssh3 = nc3.variables["RV"][it,0,:,:]
        cs3 = plt.contourf(clon2, clat2, ssh3, levels=levels, cmap=cmap, extend='both')

        cbaxes = fig.add_axes([0.1, 0.05, 0.8, 0.03])
        plt.colorbar(orientation='horizontal', cax=cbaxes)

        print('printing frame:', it)
        fig.savefig('movie/ssh_%(number)04d.png'%{'number': it})
        plt.close()

    nc.close()

