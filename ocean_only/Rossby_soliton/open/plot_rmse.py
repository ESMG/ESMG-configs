import numpy as np
import re
#import xarray as xr
import netCDF4
import os
import sys
import subprocess
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

def readtext(filename):
    f = open(filename, 'r')
    # Eat first two lines
    f.readline()
    f.readline()

    ttime = []
    energy = []
    msl = []
    mass = []
    for line in f:
        a, b, c, d, e, f, g, h = re.split(',\s+', line)
        ttime.append(float(b))
        # Eat the "En "
        d = d[3:]
        energy.append(float(d))
        f = f[3:]
        msl.append(float(f))
        g = g[5:]
        mass.append(float(g))
    ttime = np.array(ttime)
    energy = np.array(energy)
    msl = np.array(msl)
    mass = np.array(mass)
    return ttime, energy, msl, mass
    f.close()

flist = [ 'ocean.stats.zero', \
          'ocean.stats.freeslip', \
          'ocean.stats.ob_tan', \
          'ocean.stats.obgrad' ]

# hard code for now
ntim = 91
ens = np.zeros((len(flist), ntim))
sealev = np.zeros((len(flist), ntim))
masses = np.zeros((len(flist), ntim))

i = 0
for file in flist:
    times, energy, msl, mass = readtext(file)
    ens[i,:] = energy
    sealev[i,:] = msl
    masses[i,:] = mass
    i += 1


fig = plt.figure(figsize=(8,6))

plt.title('Energy (m2 s-2)')
plt.plot(times[:], ens[0,:], 'r-.', label = 'Zero')
plt.plot(times[:], ens[1,:], 'b-.', label = 'Freeslip')
plt.plot(times[:], ens[2,:], 'g-.', label = 'Oblique_tan')
plt.plot(times[:], ens[3,:], 'k--', label = 'Oblique_grad')
plt.legend(loc=1)
fig.savefig('Energy_plot.png')
plt.close()

fig = plt.figure(figsize=(8,6))

plt.title('Mean Sea Level (m)')
plt.plot(times[:], sealev[0,:], 'r-.', label = 'Zero')
plt.plot(times[:], sealev[1,:], 'b-.', label = 'Freeslip')
plt.plot(times[:], sealev[2,:], 'g-.', label = 'Oblique_tan')
plt.plot(times[:], sealev[3,:], 'k--', label = 'Oblique_grad')
plt.legend(loc=1)
fig.savefig('MSL_plot.png')
plt.close()

fig = plt.figure(figsize=(8,6))

plt.title('Mass (kg)')
plt.plot(times[:], masses[0,:], 'r-.', label = 'Zero')
plt.plot(times[:], masses[1,:], 'b-.', label = 'Freeslip')
plt.plot(times[:], masses[2,:], 'g-.', label = 'Oblique_tan')
plt.plot(times[:], masses[3,:], 'k--', label = 'Oblique_grad')
plt.legend(loc=1)
fig.savefig('Mass_plot.png')
plt.close()

