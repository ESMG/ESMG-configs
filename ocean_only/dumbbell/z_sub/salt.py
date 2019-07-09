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
p_salt=nc.Dataset(path_parent).variables['salt']
salt=nc.Dataset(exp_path).variables['salt']
nt_p=p_salt.shape[0]
nt=salt.shape[0]

x1=nc.Dataset(path_parent).variables['xh'][:]
x2=nc.Dataset(exp_path).variables['xh'][:]
y1=nc.Dataset(path_parent).variables['yh'][:]
y2=nc.Dataset(exp_path).variables['yh'][:]

i_start=int(sys.argv[1])
i_skip=int(sys.argv[2])


def salt_sfc(i):
    return salt[i,0,:]
def p_salt_sfc(i):
    return p_salt[i,0,:]

i=i_start
im1 = ax1.imshow(p_salt_sfc(i), animated=True,cmap=plt.cm.bwr,interpolation='spline16',vmin=35,vmax=36)
im2 = ax2.imshow(salt_sfc(i), animated=True,cmap=plt.cm.bwr,interpolation='spline16',vmin=35,vmax=36)


ax1.plot([40,40],[0,20],color='k')
ax1.plot([80,80],[0,20],color='k')
ax1.set_title('Layer 1  Salt (psu)')
ax2.set_xlim(-40,80)

def updatefig(*args):
    global i
    i += i_skip
    nt_min = min(nt_p,nt)
    if i<nt_min:
        im1.set_array(p_salt_sfc(i))
    if i<nt_min:
        im2.set_array(salt_sfc(i))
    if i>=nt_min:
        global stop
#    im.title('Layer 1 Relative Vorticity at t= '+str(i))
    return im1,im2,

ani = animation.FuncAnimation(fig, updatefig, interval=5, blit=True,frames=np.minimum(nt_p,nt))
Wr=animation.writers['ffmpeg']
wr=Wr(fps=15,bitrate=1800)
#ani.save('salt.mp4',writer=wr)
plt.show()
