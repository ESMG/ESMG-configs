#!/bin/csh -v

ncra -O -d Time,360, prog.nc prog_avg.nc
ncks -O -d xq,21,21 -v u prog_avg.nc west.nc
ncks -d xh,21,21 -v SSH -A  prog_avg.nc west.nc
ncks -d xh,21,21 -v salt -A  prog_avg.nc west.nc
ncks -d xh,21,21 -v h -A  prog_avg.nc west.nc
ncrename -v u,u_segment_001 west.nc
ncrename -v SSH,zeta_segment_001 west.nc
ncrename -v h,dz_u_segment_001 west.nc
ncks -d xh,21,21 -v h -A  prog_avg.nc west.nc
ncrename -v h,dz_salt_segment_001 west.nc
ncrename -v salt,salt_segment_001 west.nc

ncks -O -d xq,41,41 -v u prog_avg.nc east.nc
ncks -d xh,42,42 -v SSH -A  prog_avg.nc east.nc
ncks -d xh,42,42 -v salt -A  prog_avg.nc east.nc
ncks -d xh,42,42 -v h -A  prog_avg.nc east.nc
ncrename -v u,u_segment_002 east.nc
ncrename -v SSH,zeta_segment_002 east.nc
ncrename -v h,dz_u_segment_002 east.nc
ncks -d xh,42,42 -v h -A  prog_avg.nc east.nc
ncrename -v h,dz_salt_segment_002 east.nc
ncrename -v salt,salt_segment_002 east.nc
