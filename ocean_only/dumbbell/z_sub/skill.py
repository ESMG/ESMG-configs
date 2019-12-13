#!/usr/bin/env python
# coding: utf-8

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import sys

pgeom=nc.Dataset('../z/ocean_geometry.nc')
geom=nc.Dataset('ocean_geometry.nc')

f=open('Codes.txt')
ExpList=[]
for line in f.readlines():
    ExpList.append(line.rstrip())
expnum=int(sys.argv[1])
f.close()

print('Calculating skill for ',ExpList[expnum],' .... ')


px=pgeom.variables['lonq']
py=pgeom.variables['latq']
pxc=pgeom.variables['lonh']
pyc=pgeom.variables['lath']
pwet=pgeom.variables['wet']

x=geom.variables['lonq']
y=geom.variables['latq']
xc=geom.variables['lonh']
yc=geom.variables['lath']
wet=geom.variables['wet']

exp=ExpList[expnum]
Prog=nc.Dataset('../z/prog.nc')
prog=nc.Dataset(exp+'/prog.nc')

prv=Prog.variables['RV']
psalt=Prog.variables['salt']
ptime=Prog.variables['Time']

rv=prog.variables['RV']
salt=prog.variables['salt']
time=prog.variables['Time']



def rvSkill():
    is_=np.where(px>=x[0])[0][0]
    ie_=np.where(px>=x[-1])[0][0]
    prv_=prv[:,:,:,is_:ie_+1]
    plt.plot(time,1.e4*prv_.mean(axis=3).mean(axis=2).mean(axis=1),label='Parent Vort')
    plt.plot(time,1.e4*rv[:].mean(axis=3).mean(axis=2).mean(axis=1),label='Regional Vort')
    diff=1.e4*(rv[:]-prv_[:])
    score=diff.std()
    print('Total Vorticity error (10-4 s-1) = ',str(score)[:5])
    return score

def saltSkill():
    is_=np.where(px>=x[0])[0][0]
    ie_=np.where(px>=x[-1])[0][0]
    psalt_=psalt[:,:,:,is_:ie_]
    diff=salt[:]-psalt_
    diff2=diff*diff
    rms=diff2.mean(axis=3).mean(axis=2).mean(axis=1)
    mn=diff.mean(axis=3).mean(axis=2).mean(axis=1)
    plt.plot(time,np.sqrt(rms),label='RMS Salt Error')
    score=rms.std()
    print('RMS Salinity error (psu) =', str(score)[:5])
    return score

plt.clf()
fig=plt.figure(1,figsize=(6,4))
rv_score=rvSkill()
salt_score=saltSkill()
plt.title(ExpList[expnum]+' Average Vorticity (10-4 s-1) and RMS Salinity error (psu)')
plt.xlabel('days')
plt.ylabel('psu or 10-4 s-1')
plt.grid()
plt.legend()
plt.ylim(-.25,0.75)
fig.savefig(exp+'/skill.png')
g=open(exp+'/score.txt','w')
g.write(str(rv_score)[:5]+','+str(salt_score)[:5]+'\n')
g.close()
