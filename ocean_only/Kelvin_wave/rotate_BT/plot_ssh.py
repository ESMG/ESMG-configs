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

clat = grd.variables["geolat"][:]
clon = grd.variables["geolon"][:]

#m = Basemap(llcrnrlon=-165.5, llcrnrlat=70.3, urcrnrlon=-128.0, urcrnrlat=71.0,\
#            rsphere=(6378137.00,6356752.3142),\
#            resolution='h', projection='lcc',\
#            lat_0=65., lat_1=70.0, lon_0=-162.)
#x, y = m(clon, clat)
levels = np.arange(-0.7, 0.7, 0.05)
cmap = plt.cm.get_cmap("PRGn")

for file in lst_file:
    print("Plotting "+file)
#   m.drawmapboundary(fill_color='0.3')
#   m.drawcoastlines()
    nc = netCDF4.Dataset(file, "r")
    time = nc.variables["time"][:]
    ntim = len(time)
    for it in range(ntim):
        fig = plt.figure()
        plt.axis([0, 1200, 0, 800])
        plt.axes().set_aspect('equal', 'datalim')
        ssh = nc.variables["e"][it,0,:,:]
        time = nc.variables["time"][it]
#       cs = m.contourf(x, y, ssh, levels=levels, cmap=cmap)
#       csa = m.contour(x, y, ssh, levels=levels, linewidths=(0.5,))
        cs = plt.contourf(clon, clat, ssh, levels=levels, cmap=cmap, extend='both')
        plt.title('Surface Elevation')
        csa = plt.contour(clon, clat, ssh, levels=levels, linewidths=(0.5,))
        plt.colorbar(orientation='horizontal')
        fig.savefig('movie/ssh_%(number)03d.png'%{'number': it})
        plt.close()

    nc.close()

