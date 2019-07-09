# IPython log file

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import sys
import pickle

path_parent='../z/save/parent_002/prog.nc'
p=nc.Dataset(path_parent)
salt=p.variables['salt']
h=p.variables['h']
days=p.variables['Time'][:-1]
days=days-days[0]
i1=39;i2=79
salt_tot=np.sum(np.sum(salt[:-1,0,:,i1:i2+1]*h[:-1,0,:,i1:i2+1],axis=2),axis=1)*1.e-6
exp_path=sys.argv[1]
e=nc.Dataset(exp_path)
salt_=e.variables['salt']
h_=e.variables['h']
salt_tot_=np.sum(np.sum(salt_[:-1,0,:,:]*h_[:-1,0,:,:],axis=2),axis=1)*1.e-6
days_=e.variables['Time'][:-1]
days_=days_-days_[0]
plt.plot(days,np.squeeze(salt_tot),label='Parent')
plt.plot(days_,np.squeeze(salt_tot_),label='Regional')
plt.legend()
plt.grid()
plt.xlabel('Model Simulation Days')
plt.ylabel('Regional Domain Total Salt (Mg)')
#plt.ylim(0,.65)
out_path=sys.argv[2]
plt.savefig(out_path)
diff=salt_tot_-salt_tot[:-1]
print('Parent')
result = {'Mean':salt_tot.mean(),'Max':salt_tot.max(),'RMS':salt_tot.std()}
print(result)
print('Regional')
result = {'Mean':salt_tot_.mean(),'Max':salt_tot_.max(),'RMS':salt_tot_.std()}
print(result)
result = {'Mean':diff.mean(),'Max':diff.max(),'RMS':diff.std()}
out_path=sys.argv[3]
pickle.dump(result,open(out_path,"wb"))
print(result)
