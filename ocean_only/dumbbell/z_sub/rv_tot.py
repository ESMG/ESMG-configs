# IPython log file

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import sys
import pickle

path_parent='../z/save/parent_002/prog.nc'
p=nc.Dataset(path_parent)
rv=p.variables['RV']
h=p.variables['h']
hq=0.25*(h+np.roll(h,shift=1,axis=3)+np.roll(h,shift=1,axis=2)+np.roll(np.roll(h,shift=1,axis=2),shift=1,axis=3))
days=p.variables['Time'][:]
days=days-days[0]
i1=39;i2=79
hq0=np.take(hq,[0],axis=2)
hq=np.concatenate((hq0,hq),axis=2)
rv_tot=np.sum(np.sum(rv[:,0,:,i1:i2+1]*hq[:,0,:,i1:i2+1],axis=2),axis=1)/np.sum(np.sum(hq[:,0,:,i1:i2+1],axis=2),axis=1)*1.e4
exp_path=sys.argv[1]
e=nc.Dataset(exp_path)
rv_=e.variables['RV']
h_=e.variables['h']
hq_=0.25*(h_+np.roll(h_,shift=1,axis=3)+np.roll(h_,shift=1,axis=2)+np.roll(np.roll(h_,shift=1,axis=2),shift=1,axis=3))
hq0=np.take(hq_,[0],axis=2)
hq_=np.concatenate((hq0,hq_),axis=2)
hq0=np.take(hq_,[0],axis=3)
hq_=np.concatenate((hq0,hq_),axis=3)
rv_tot_=np.sum(np.sum(rv_[:,0,:,:]*hq_[:,0,:,:],axis=2),axis=1)/np.sum(np.sum(hq_[:,0,:,:],axis=2),axis=1)*1.e4
days_=e.variables['Time'][:]
days_=days_-days_[0]
plt.plot(days,np.squeeze(rv_tot),label='Parent')
plt.plot(days_,np.squeeze(rv_tot_),label='Regional')
plt.legend()
plt.grid()
plt.xlabel('Model Simulation Days')
plt.ylabel('Regional Domain Total Vorticity (10**4 s-1)')
plt.ylim(0,.65)
out_path=sys.argv[2]
plt.savefig(out_path)
diff=rv_tot_-rv_tot[:-1]
result = {'Mean':diff.mean(),'Max':diff.max(),'RMS':diff.std()}
out_path=sys.argv[3]
pickle.dump(result,open(out_path,"wb"))
print(result)
