import numpy as np
import sys
from subprocess import call
import xarray as xr


output_file = 'forcing.nc'

compress = True
if compress:
   fileformat, zlib, complevel, area_dtype = 'NETCDF4', True, 1, 'f4'
else:
   fileformat, zlib, complevel, area_dtype = 'NETCDF3_64BIT_OFFSET', None, None, 'd'

NJ = 2
NI = 2
width = 10
edge_val = 1.e-6
times = np.array([15., 45., 75., 105., 135., 165., 195., 225., 255., 285., 315., 345. ])
lon = np.array([0., 20. ])
lat = np.array([70., 80. ])
tair_time = np.array([-27., -25., -22., -15., -2., 0.,
              1., -.5, -1., -2., -15., -27. ])
sw_time = np.array([ 0., 0., 30.7, 160., 286., 310.,
            220., 145., 60., 6., 0., 0. ])
lw_time = np.array([ 168., 166., 166., 187., 244., 291.,
            309., 302., 267., 225., 181., 176.  ])
hu_time = np.array([ .0004, .0005, .0005, .001, .0025, .0035,
            .004, .005, .0035, .002, .0015, .0005 ])
sn_time = np.array([ 1.1e-6, 1.1e-6, 1.1e-6, 1.1e-6, 6.4e-6, 0.,
            0., 0., 1.64e-5, 1.64e-5, 1.1e-6, 1.1e-6 ])

press = 101325 * np.ones((12,NJ,NI))
tair = np.broadcast_to(tair_time, (NJ,NI,12)).T + 273.16
sw = np.broadcast_to(sw_time, (NJ,NI,12)).T
lw = np.broadcast_to(lw_time, (NJ,NI,12)).T
qair = np.broadcast_to(hu_time, (NJ,NI,12)).T
snow = np.broadcast_to(sn_time, (NJ,NI,12)).T
rain = np.zeros((12,NJ,NI))
uw = np.zeros((12,NJ,NI))
vw = np.zeros((12,NJ,NI))

idtime = xr.DataArray(times, dims=['time'])
idtime.attrs["units"] = "days since 1000-01-01"
idtime.attrs["calendar"] = "thirty_day_months"
idtime.attrs["modulo"] = "360"
#idtime.attrs["modulo_begin"] = "0"
#idtime.attrs["modulo_end"] = "360"

idlon = xr.DataArray(lon, dims=['lon'])
idlon.attrs["units"] = "degrees_east"

idlat = xr.DataArray(lat, dims=['lat'])
idlat.attrs["units"] = "degrees_north"

idp = xr.DataArray(press, dims=['time', 'lat', 'lon'])
idp.attrs["units"] = "Pa"
idp.attrs["coordinates"] = "lon lat"
idp.attrs["time"] = "time"

idt = xr.DataArray(tair, dims=['time', 'lat', 'lon'])
idt.attrs["units"] = "deg_K"
idt.attrs["coordinates"] = "lon lat"
idt.attrs["time"] = "time"

idlw = xr.DataArray(lw, dims=['time', 'lat', 'lon'])
idlw.attrs["units"] = "W m-2"
idlw.attrs["coordinates"] = "lon lat"
idlw.attrs["time"] = "time"

idsw = xr.DataArray(sw, dims=['time', 'lat', 'lon'])
idsw.attrs["units"] = "W m-2"
idsw.attrs["coordinates"] = "lon lat"
idsw.attrs["time"] = "time"

idhu = xr.DataArray(qair, dims=['time', 'lat', 'lon'])
idhu.attrs["units"] = "1"
idhu.attrs["coordinates"] = "lon lat"
idhu.attrs["time"] = "time"

idsn = xr.DataArray(snow, dims=['time', 'lat', 'lon'])
idsn.attrs["units"] = "kg m-2 s-1"
idsn.attrs["coordinates"] = "lon lat"
idsn.attrs["time"] = "time"

idra = xr.DataArray(rain, dims=['time', 'lat', 'lon'])
idra.attrs["units"] = "kg m-2 s-1"
idra.attrs["coordinates"] = "lon lat"
idra.attrs["time"] = "time"

iduw = xr.DataArray(uw, dims=['time', 'lat', 'lon'])
iduw.attrs["units"] = "m s-1"
iduw.attrs["coordinates"] = "lon lat"
iduw.attrs["time"] = "time"

idvw = xr.DataArray(vw, dims=['time', 'lat', 'lon'])
idvw.attrs["units"] = "m s-1"
idvw.attrs["coordinates"] = "lon lat"
idvw.attrs["time"] = "time"

base = xr.Dataset(data_vars = {"time" : idtime,
                               "lon" : idlon,
                               "lat" : idlat,
                               "Pair" : idp,
                               "Tair" : idt,
                               "Qair" : idhu,
                               "lwrad" : idlw,
                               "swrad" : idsw,
                               "rain" : idra,
                               "snow" : idsn,
                               "Uwind" : iduw,
			       "Vwind" : idvw})
base.attrs["grid_type"] = "regional MOM6"
base.attrs["grid"] = "ice_box"

comp = dict(zlib=zlib, complevel=complevel, _FillValue=None)
encoding = {var: comp for var in base.data_vars}
base.to_netcdf(
    output_file,
    unlimited_dims='time',
    format=fileformat,
    encoding=encoding
)
