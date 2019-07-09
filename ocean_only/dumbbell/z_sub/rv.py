import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
exp_path = sys.argv[3]
path_parent='../z/save/parent_002/prog.nc'
p_rv=nc.Dataset(path_parent).variables['RV']
rv=nc.Dataset(exp_path).variables['RV']
nt_p=p_rv.shape[0]
nt=rv.shape[0]

x1=nc.Dataset(path_parent).variables['xh'][:]
x2=nc.Dataset(exp_path).variables['xh'][:]
y1=nc.Dataset(path_parent).variables['yh'][:]
y2=nc.Dataset(exp_path).variables['yh'][:]

i_start=int(sys.argv[1])
i_skip=int(sys.argv[2])


def rv_sfc(i):
    return rv[i,0,:]*1.e5
def p_rv_sfc(i):
    return p_rv[i,0,:]*1.e5

i=i_start
im1 = ax1.imshow(p_rv_sfc(i), animated=True,cmap=plt.cm.bwr,interpolation='spline16',vmin=-5,vmax=5)
im2 = ax2.imshow(rv_sfc(i), animated=True,cmap=plt.cm.bwr,interpolation='spline16',vmin=-5,vmax=5)


ax1.plot([40,40],[0,20],color='k')
ax1.plot([80,80],[0,20],color='k')
ax1.set_title('Layer 1  Vorticity 10**-4 m s-2')
ax2.set_xlim(-40,80)

def updatefig(*args):
    global i
    i += i_skip
    nt_min = min(nt_p,nt)
    if i<nt_min:
        im1.set_array(p_rv_sfc(i))
    if i<nt_min:
        im2.set_array(rv_sfc(i))
    if i>=nt_min:
        global stop
#    im.title('Layer 1 Relative Vorticity at t= '+str(i))
    return im1,im2,

ani = animation.FuncAnimation(fig, updatefig, interval=5, blit=True,frames=np.minimum(nt_p,nt))
Wr=animation.writers['ffmpeg']
wr=Wr(fps=15,bitrate=1800)
#ani.save('rv.mp4',writer=wr)
plt.show()
