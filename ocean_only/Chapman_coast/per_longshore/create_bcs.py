# IPython log file

import netCDF4 as nc
import numpy as np

n = nc.Dataset('north.nc','w',format='NETCDF3_64BIT')
s = nc.Dataset('south.nc','w',format='NETCDF3_64BIT')
p = nc.Dataset('prog.nc','r')
grd = nc.Dataset('ocean_geometry.nc','r')
ic = nc.Dataset('MOM_IC.nc','r')

i = 15
yh = p.variables['yh'][i]
yq = p.variables['yq'][i+1]
xh = p.variables['xh'][:]
xq = p.variables['xq'][:]

FillVal=-1.e20

for e,cnum in zip((n,s),('002','003')):
    tdim = e.createDimension('time',None)
    tdimv = e.createVariable('time','f8',('time'),fill_value=FillVal)
    tdimv.units = 'seconds since 0001-01-01 00:00:00'
    tdimv.cartesian_axis = 'T'
    tdimv.calendar_type = 'julian'

    zl = p.variables['zl'][:]
    zdim = e.createDimension('zl',len(zl))
    zv = e.createVariable('zl','f8',('zl'))
    zv.cartesian_axis = 'Z'
    zv[:] = zl
    ydim = e.createDimension('yh',1)
    yv = e.createVariable('yh','f8',('yh'))
    yv.cartesian_axis = 'Y'
    yv[:] = yh
    yqdim = e.createDimension('yq',1)
    yqv = e.createVariable('yq','f8',('yq'))
    yqv.cartesian_axis = 'Y'
    yqv[:] = yq
    xdim = e.createDimension('xh',len(xh))
    xv = e.createVariable('xh','f8',('xh'))
    xv.cartesian_axis = 'X'
    xv[:] = xh
    xqdim = e.createDimension('xq',len(xq))
    xqv = e.createVariable('xq','f8',('xq'))
    xqv.cartesian_axis = 'X'
    xqv[:] = xq

    print('segnam,xh,xq=',cnum,xh,xq)
    vnam = 'zeta_segment_'+cnum
    zvv = e.createVariable(vnam,'f8',('time','yq','xh'),fill_value=FillVal)
#   vnam = 'salt_segment_'+cnum
#   sv = e.createVariable(vnam,'f8',('time','zl','yh','xq'),fill_value=FillVal)
#   vnam = 'dz_salt_segment_'+cnum
#   hsv = e.createVariable(vnam,'f8',('time','zl','yh','xq'),fill_value=FillVal)
    vnam = 'u_segment_'+cnum
    uv = e.createVariable(vnam,'f8',('time','zl','yq','xq'),fill_value=FillVal)
#   vnam = 'vhbt_segment_'+cnum
#   vhbtv = e.createVariable(vnam,'f8',('time','yq','xh'),fill_value=FillVal)
    vnam = 'dz_u_segment_'+cnum
    huv = e.createVariable(vnam,'f8',('time','zl','yq','xq'),fill_value=FillVal)
    vnam = 'v_segment_'+cnum
    vv = e.createVariable(vnam,'f8',('time','zl','yq','xh'),fill_value=FillVal)
    vnam = 'dz_v_segment_'+cnum
    hvv = e.createVariable(vnam,'f8',('time','zl','yq','xh'),fill_value=FillVal)
    vnam = 'dudy_segment_'+cnum
    dudyv = e.createVariable(vnam,'f8',('time','zl','yq','xq'),fill_value=FillVal)
    vnam = 'dz_dudy_segment_'+cnum
    hdudyv = e.createVariable(vnam,'f8',('time','zl','yq','xq'),fill_value=FillVal)

    zvv[0] = 0.5*(ic.variables['sfc'][:,i,:]+ic.variables['sfc'][:,i+1,:])
#   sv[0] = 0.5*(ic.variables['Salt'][:,:,:,i]+ic.variables['Salt'][:,:,:,i+1])
#   hsv[0] = 0.5*(ic.variables['h'][:,:,i,:]+ic.variables['h'][:,:,i+1,:])
    vv[0] = ic.variables['v'][:,:,i+1,:]
#   uv[0] = ic.variables['uh'][:,:,:,i+1]/hsv[0]/ (g.variables['dyCu'][:,i+1].reshape([1,1,20]))
#   vhbtv[0] = ic.variables['vhbt_IC'][:,i+1,:]
    hvv[0] = 0.5*(ic.variables['h'][:,:,i,:]+ic.variables['h'][:,:,i+1,:])
    uv[0] = 0.5*(ic.variables['u'][:,:,i,:]+ic.variables['u'][:,:,i+1,:])
    hijp = np.roll(ic.variables['h'][:,:,i,:],shift=-1,axis=2)
    hipjp = np.roll(ic.variables['h'][:,:,i+1,:],shift=-1,axis=2)
    hij = ic.variables['h'][:,:,i,:]
    hipj = ic.variables['h'][:,:,i+1,:]
    a = 0.25*(hij+hipj+hijp+hipjp)
    a0 = a[:,:,0][:,:,np.newaxis]
    a = np.concatenate((a0,a),axis=2)
    a[:,:,0] = 2*a[:,:,1] - a[:,:,2]
    a[:,:,-1] = 2*a[:,:,-2] - a[:,:,-3]
    print('a=', a, a.shape)
    huv[0] = a
    hdudyv[0] = a
#   dx = grd.variables['dxBu'][i+1,:]
#   dx = np.tile(dx[np.newaxis,np.newaxis,:],(1,hvv.shape[1],1))
#   a = (ic.variables['u'][:,:,i+1,:]-ic.variables['u'][:,:,i,:])
#   dudyv[0] = a/dy
    dudyv[0] = 0.0
    tdimv[0] = 0.0

    zvv[1:] = 0.5*(p.variables['e'][:,0,i,:]+p.variables['e'][:,0,i+1,:])
#   sv[1:] = 0.5*(p.variables['salt'][:,:,:,i]+p.variables['salt'][:,:,:,i+1])
#   hsv[1:] = 0.5*(p.variables['h'][:,:,i,:]+p.variables['h'][:,:,i+1,:])
    vv[1:] = p.variables['v'][:,:,i+1,:]
#   uv[1:] = p.variables['uh'][:,:,:,i+1]/hsv[1:]/ (g.variables['dyCu'][:,i+1].reshape([1,1,20]))
#   vhbtv[1:] = p.variables['vhbt'][:,i+1,:]
    hvv[1:] = 0.5*(p.variables['h'][:,:,i,:]+p.variables['h'][:,:,i+1,:])
    uv[1:] = 0.5*(p.variables['u'][:,:,i,:]+p.variables['u'][:,:,i+1,:])
    hijp = np.roll(p.variables['h'][:,:,i,:],shift=-1,axis=2)
    hipjp = np.roll(p.variables['h'][:,:,i+1,:],shift=-1,axis=2)
    hij = p.variables['h'][:,:,i,:]
    hipj = p.variables['h'][:,:,i+1,:]
    a = 0.25*(hij+hipj+hijp+hipjp)
    a0 = a[:,:,0][:,:,np.newaxis]
    a = np.concatenate((a0,a),axis=2)
    huv[1:] = a
    hdudyv[1:] = a
#   dx = grd.variables['dxBu'][:,i+1]
#   dx = np.tile(dx[np.newaxis,np.newaxis,:],(hvv.shape[0]-1,hvv.shape[1],1))
#   a = (p.variables['v'][:,:,:,i+1]-p.variables['v'][:,:,:,i])
#   dudyv[1:] = a/dx
    dudyv[1:] = 0.0
    tdimv[1:] = p.variables['time'][:]

#   for tp in np.arange(2):
#       nt =  tdimv.shape[0]
#       zvv[nt] = zvv[nt-1]
##      sv[nt] = sv[nt-1]
#       hsv[nt] = hsv[nt-1]
#       uv[nt] = uv[nt-1]
#       uhbtv[nt] = uhbtv[nt-1]
#       huv[nt] = huv[nt-1]
#       vv[nt] = vv[nt-1]
#       hvv[nt] = hvv[nt-1]
#       dudyv[nt] = dudyv[nt-1]
#       tdimv[nt] = 2*tdimv[nt-1]-tdimv[nt-2]

    e.sync()
    e.close()
