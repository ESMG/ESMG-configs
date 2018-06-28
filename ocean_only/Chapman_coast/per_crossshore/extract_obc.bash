#!/bin/bash
# Extract boundary conditions for the child domain from the output of
# the parent domain.

ncks -O -d yh,15,15 -d zi,0,0 -v e prog.nc ends.nc
ncks -d yh,15,15 -v h -A  prog.nc ends.nc
ncks -d yq,15,15 -v v -A  prog.nc ends.nc
ncatted -a modulo,time,c,c,' ' ends.nc
ncrename -v e,zeta_segment_002 ends.nc
ncrename -v v,v_segment_002 ends.nc
ncrename -v h,dz_v_segment_002 ends.nc

ncks -d yh,15,15 -d zi,0,0 -v e -A  prog.nc ends.nc
ncks -d yh,15,15 -v h -A  prog.nc ends.nc
ncks -d yq,15,15 -v v -A  prog.nc ends.nc
ncrename -v e,zeta_segment_003 ends.nc
ncrename -v v,v_segment_003 ends.nc
ncrename -v h,dz_v_segment_003 ends.nc

