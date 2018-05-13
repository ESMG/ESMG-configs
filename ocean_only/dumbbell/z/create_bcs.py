# IPython log file

import netCDF4 as nc
import numpy as np

e=nc.Dataset('east.nc','w',format='NETCDF3_CLASSIC')
w=nc.Dataset('west.nc','w',format='NETCDF3_CLASSIC')
p=nc.Dataset('prog.nc','r')
grd=nc.Dataset('ocean_geometry.nc','r')
ic=nc.Dataset('MOM_IC.nc','r')

yh=p.variables['yh'][:]
yq=p.variables['yq'][:]

FillVal=-1.e20

for r,i,cnum in zip((e,w),(79,39),('002','001')):
    tdim=r.createDimension('Time',None)
    tdimv=r.createVariable('Time','f8',('Time'),fill_value=FillVal)
    tdimv.units='days since 0001-01-01 00:00:00'
    tdimv.cartesian_axis='T'
    tdimv.calendar_type='julian'
    zl=p.variables['zl'][:]
    xh=p.variables['xh'][i]
    xq=p.variables['xq'][i+1]

    print('segnam,xh,xq=',cnum,xh,xq)
    zdim=r.createDimension('zl',len(zl))
    zv=r.createVariable('zl','f8',('zl'))
    zv.cartesian_axis='Z'
    zv[:]=zl
    xdim=r.createDimension('xh',1)
    xv=r.createVariable('xh','f8',('xh'))
    xv.cartesian_axis='X'
    xv[:]=xh
    xqdim=r.createDimension('xq',1)
    xqv=r.createVariable('xq','f8',('xq'))
    xqv.cartesian_axis='X'
    xqv[:]=xq
    ydim=r.createDimension('yh',len(yh))
    yv=r.createVariable('yh','f8',('yh'))
    yv.cartesian_axis='Y'
    yv[:]=yh
    yqdim=r.createDimension('yq',len(yq))
    yqv=r.createVariable('yq','f8',('yq'))
    yqv.cartesian_axis='Y'    
    yqv[:]=yq
    vnam='zeta_segment_'+cnum                    
    zvv=r.createVariable(vnam,'f8',('Time','yh','xq'),fill_value=FillVal)
    vnam='salt_segment_'+cnum                    
    sv=r.createVariable(vnam,'f8',('Time','zl','yh','xq'),fill_value=FillVal)
    vnam='dz_salt_segment_'+cnum                    
    hsv=r.createVariable(vnam,'f8',('Time','zl','yh','xq'),fill_value=FillVal)    
    vnam='u_segment_'+cnum                    
    uv=r.createVariable(vnam,'f8',('Time','zl','yh','xq'),fill_value=FillVal)
    vnam='dz_u_segment_'+cnum                    
    huv=r.createVariable(vnam,'f8',('Time','zl','yh','xq'),fill_value=FillVal)
    vnam='v_segment_'+cnum                    
    vv=r.createVariable(vnam,'f8',('Time','zl','yq','xq'),fill_value=FillVal)
    vnam='dz_v_segment_'+cnum                    
    hvv=r.createVariable(vnam,'f8',('Time','zl','yq','xq'),fill_value=FillVal)
    vnam='dvdx_segment_'+cnum                    
    dvdxv=r.createVariable(vnam,'f8',('Time','zl','yq','xq'),fill_value=FillVal)
    vnam='dz_dvdx_segment_'+cnum                    
    hdvdxv=r.createVariable(vnam,'f8',('Time','zl','yq','xq'),fill_value=FillVal)        
#    vnam='uhbt_segment_'+cnum                    
#    uhbtv=r.createVariable(vnam,'f8',('Time','yh','xq'),fill_value=FillVal)
    
    zvv[0]=0.5*(ic.variables['sfc'][:,:,i]+ic.variables['sfc'][:,:,i+1])
    sv[0]=0.5*(ic.variables['Salt'][:,:,:,i]+ic.variables['Salt'][:,:,:,i+1])
    hsv[0]=0.5*(ic.variables['h'][:,:,:,i]+ic.variables['h'][:,:,:,i+1])
    uv[0]=ic.variables['u'][:,:,:,i+1]
#    uhbtv[0]=ic.variables['uhbt_IC'][:,:,i+1]    
    huv[0]=0.5*(ic.variables['h'][:,:,:,i]+ic.variables['h'][:,:,:,i+1])
    vv[0]=0.5*(ic.variables['v'][:,:,:,i]+ic.variables['v'][:,:,:,i+1])
    hijp=np.roll(ic.variables['h'][:,:,:,i],shift=-1,axis=2)
    hipjp=np.roll(ic.variables['h'][:,:,:,i+1],shift=-1,axis=2)
    hij=ic.variables['h'][:,:,:,i]
    hipj=ic.variables['h'][:,:,:,i+1]
    a=0.25*(hij+hipj+hijp+hipjp)
    a0=a[:,:,0][:,:,np.newaxis]
    a=np.concatenate((a0,a),axis=2)
    hvv[0]=a
    dx=grd.variables['dxBu'][:,i+1]
    dx=np.tile(dx[np.newaxis,np.newaxis,:],(1,hvv.shape[1],1))
    a=(ic.variables['v'][:,:,:,i+1]-ic.variables['v'][:,:,:,i])
    dvdxv[0]=a/dx
    tdimv[0]=0.0
    hdvdxv[0]=hvv[0]
    
    hvar='hav'
    zvv[1:]=0.5*(p.variables['ssh'][:,:,i]+p.variables['ssh'][:,:,i+1])
    sv[1:]=0.5*(p.variables['salt'][:,:,:,i]+p.variables['salt'][:,:,:,i+1])
    hsv[1:]=0.5*(p.variables[hvar][:,:,:,i]+p.variables[hvar][:,:,:,i+1])    
    uv[1:]=p.variables['u'][:,:,:,i+1]
#    uhbtv[1:]=p.variables['uhbt'][:,:,i+1]        
    huv[1:]=0.5*(p.variables[hvar][:,:,:,i]+p.variables[hvar][:,:,:,i+1])
    vv[1:]=0.5*(p.variables['v'][:,:,:,i]+p.variables['v'][:,:,:,i+1])
    hijp=np.roll(p.variables[hvar][:,:,:,i],shift=-1,axis=2)
    hipjp=np.roll(p.variables[hvar][:,:,:,i+1],shift=-1,axis=2)
    hij=p.variables[hvar][:,:,:,i]
    hipj=p.variables[hvar][:,:,:,i+1]
    a=0.25*(hij+hipj+hijp+hipjp)
    a0=a[:,:,0][:,:,np.newaxis]
    a=np.concatenate((a0,a),axis=2)
    hvv[1:]=a
    dx=grd.variables['dxBu'][:,i+1]
    dx=np.tile(dx[np.newaxis,np.newaxis,:],(hvv.shape[0]-1,hvv.shape[1],1))
    a=(p.variables['v'][:,:,:,i+1]-p.variables['v'][:,:,:,i])
    dvdxv[1:]=a/dx
    tdimv[1:]=p.variables['Time'][:]
    hdvdxv[1:]=hvv[1:]
    
    for tp in np.arange(2):
        nt= tdimv.shape[0]
        zvv[nt]=zvv[nt-1]
        sv[nt]=sv[nt-1]
        hsv[nt]=hsv[nt-1]
        uv[nt]=uv[nt-1]
#        uhbtv[nt]=uhbtv[nt-1]        
        huv[nt]=huv[nt-1]
        vv[nt]=vv[nt-1]
        hvv[nt]=hvv[nt-1]
        dvdxv[nt]=dvdxv[nt-1]
        tdimv[nt]=2*tdimv[nt-1]-tdimv[nt-2]
        hdvdxv[nt]=hvv[nt]
    r.sync()
    r.close()
