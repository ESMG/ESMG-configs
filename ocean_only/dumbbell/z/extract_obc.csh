source ~/ifort

#ncra -O -d Time,360, prog.nc prog_late.nc
ncks -O -d Time,360, prog.nc prog_late.nc
ncks -O -d xq,41,41 -v u prog_late.nc west.nc
ncks -d xh,41,41 -v SSH -A  prog_late.nc west.nc
ncks -d xh,41,41 -v salt -A  prog_late.nc west.nc
ncks -d xh,41,41 -v h -A  prog_late.nc west.nc
ncatted -a modulo,Time,c,c,' ' west.nc
ncrename -v u,u_segment_001 west.nc
ncrename -v SSH,zeta_segment_001 west.nc
ncrename -v h,dz_u_segment_001 west.nc
ncks -d xh,41,41 -v h -A  prog_late.nc west.nc
ncrename -v h,dz_salt_segment_001 west.nc
ncrename -v salt,salt_segment_001 west.nc

ncks -O -d xq,81,81 -v u prog_late.nc east.nc
ncks -d xh,82,82 -v SSH -A  prog_late.nc east.nc
ncks -d xh,82,82 -v salt -A  prog_late.nc east.nc
ncks -d xh,82,82 -v h -A  prog_late.nc east.nc
ncatted -a modulo,Time,c,c,' ' east.nc
ncrename -v u,u_segment_002 east.nc
ncrename -v SSH,zeta_segment_002 east.nc
ncrename -v h,dz_u_segment_002 east.nc
ncks -d xh,82,82 -v h -A  prog_late.nc east.nc
ncrename -v h,dz_salt_segment_002 east.nc
ncrename -v salt,salt_segment_002 east.nc
