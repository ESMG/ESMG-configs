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
lst = subprocess.getoutput('ls 19800110.ocean_daily.nc')
lst = lst.split()
lst_file = lst_file + lst

#grd = pyroms_toolbox.BGrid_GFDL.get_nc_BGrid_GFDL('prog.nc')
grd = netCDF4.Dataset('sea_ice_geometry.nc', "r")

clat = grd.variables["geolat"][:]
clon = grd.variables["geolon"][:]

m = Basemap(llcrnrlon=-121., llcrnrlat=17., urcrnrlon=-125.0, urcrnrlat=53.0,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='h', projection='lcc',\
            lat_0=30., lat_1=40.0, lon_0=-78.)
x, y = m(clon, clat)
levels = np.arange(32.5, 35.5, 0.05)
cmap = plt.cm.get_cmap("plasma_r")

for file in lst_file:
    print("Plotting "+file)
    nc = netCDF4.Dataset(file, "r")
    time = nc.variables["time"][:]
    ntim = len(time)
#   for it in range(10):
    for it in range(0,ntim,30):
        fig = plt.figure(figsize=(4,9))
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
#       ax.axis(xmin=-300,xmax=300)
#       m.drawmapboundary(fill_color='0.3')
        m.drawcoastlines()
        ssh = nc.variables["sss"][it,:,:]
        time = nc.variables["time"][it]
        cs = m.contourf(x, y, ssh, levels=levels, cmap=cmap, extend='both')
#       csa = m.contour(x, y, ssh, levels=levels, linewidths=(0.5,))
#       cs = plt.contourf(clon, clat, ssh, levels=levels, cmap=cmap, extend='both')
        plt.title('Surface salt')
#       csa = plt.contour(clon, clat, ssh, levels=levels, linewidths=(0.5,))

        cbaxes = fig.add_axes([0.1, 0.05, 0.8, 0.02])
        plt.colorbar(orientation='horizontal', cax=cbaxes)

        print('printing frame:', it)
        fig.savefig('movie/sss_%(number)04d.png'%{'number': it})
        plt.close()

    nc.close()

