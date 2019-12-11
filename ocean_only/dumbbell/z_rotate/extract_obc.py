#!/bin/env python
# Extract boundary conditions for the child domain from the output of
# the parent domain. Run this after extract_obc.bash.
import numpy as np
import netCDF4
import os
import sys
import subprocess
import numpy as np
from datetime import datetime

grd = netCDF4.Dataset('ocean_geometry.nc', "r")
prog = netCDF4.Dataset('prog.nc', "r")
north = netCDF4.Dataset('north.nc', 'a')
south = netCDF4.Dataset('south.nc', 'a')
spval = 1.e20

new = True
if new:
    south.createVariable('dudy_segment_001', 'f8', ('Time', 'zl', 'yq', 'xq'), fill_value=spval)
    south.variables['dudy_segment_001'].long_name = 'Part of vorticity.'
    south.variables['dudy_segment_001'].units = '1/s'

    south.createVariable('dz_dudy_segment_001', 'f8', ('Time', 'zl', 'yq', 'xq'), fill_value=spval)
    south.variables['dz_dudy_segment_001'].long_name = 'Layer thicknesses.'
    south.variables['dz_dudy_segment_001'].units = 'm'

    north.createVariable('dudy_segment_002', 'f8', ('Time', 'zl', 'yq', 'xq'), fill_value=spval)
    north.variables['dudy_segment_002'].long_name = 'Part of vorticity.'
    north.variables['dudy_segment_002'].units = '1/s'

    north.createVariable('dz_dudy_segment_002', 'f8', ('Time', 'zl', 'yq', 'xq'), fill_value=spval)
    north.variables['dz_dudy_segment_002'].long_name = 'Layer thicknesses.'
    north.variables['dz_dudy_segment_002'].units = 'm'

# Whole grid
u = prog.variables['u'][:]
h = prog.variables['h'][:]
salt = prog.variables['salt'][:]
SSH = prog.variables['SSH'][:]
dy = grd.variables['dyBu'][:]

# Segment 1
#print(u.shape, dy.shape)
dudy = (u[:,:,40,:] - u[:,:,39,:]) / dy[40,:]
useg = 0.5*(u[:,:,40,:] + u[:,:,39,:])
hseg = 0.5*(h[:,:,40,:] + h[:,:,39,:])
hqseg = np.zeros(useg.shape)
hqseg[:,:,0:3] = hseg[:,:,0:3]
hqseg[:,:,18:] = hseg[:,:,17:]
hqseg[:,:,3:18] = 0.5*(hseg[:,:,2:17] + hseg[:,:,3:18])
saltseg = 0.5*(salt[:,:,40,:] + salt[:,:,39,:])
sshseg = 0.5*(SSH[:,40,:] + SSH[:,39,:])

south.variables['dudy_segment_001'][:] = dudy
south.variables['dz_dudy_segment_001'][:] = hqseg
south.variables['u_segment_001'][:] = useg
south.variables['dz_u_segment_001'][:] = hqseg
south.variables['salt_segment_001'][:] = saltseg
south.variables['dz_salt_segment_001'][:] = hseg
south.variables['dz_v_segment_001'][:] = hseg
south.variables['zeta_segment_001'][:] = sshseg
south.close()

# Segment 2
dudy = (u[:,:,80,:] - u[:,:,79,:]) / dy[80,:]
useg = 0.5*(u[:,:,80,:] + u[:,:,79,:])
hseg = 0.5*(h[:,:,80,:] + h[:,:,79,:])
hqseg = np.zeros(useg.shape)
hqseg[:,:,0:3] = hseg[:,:,0:3]
hqseg[:,:,18:] = hseg[:,:,17:]
hqseg[:,:,3:18] = 0.5*(hseg[:,:,2:17] + hseg[:,:,3:18])
saltseg = 0.5*(salt[:,:,80,:] + salt[:,:,79,:])
sshseg = 0.5*(SSH[:,80,:] + SSH[:,79,:])

north.variables['dudy_segment_002'][:] = dudy
north.variables['dz_dudy_segment_002'][:] = hqseg
north.variables['u_segment_002'][:] = useg
north.variables['dz_u_segment_002'][:] = hqseg
north.variables['salt_segment_002'][:] = saltseg
north.variables['dz_salt_segment_002'][:] = hseg
north.variables['dz_v_segment_002'][:] = hseg
north.variables['zeta_segment_002'][:] = sshseg
north.close()
