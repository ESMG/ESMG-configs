#!/bin/bash
# Extract boundary conditions for the child domain from the output of
# the parent domain.

ncks -O -d lath,15,15 -d Interface,0,0 -v eta MOM_IC.nc ends_1.nc
ncks -d lath,15,15 -v h -A  MOM_IC.nc ends_1.nc
ncks -d latq,15,15 -v v -A  MOM_IC.nc ends_1.nc
ncrename -v eta,e ends_1.nc
ncrename -d Time,time -v Time,time ends_1.nc
ncrename -v lonh,xh -v lath,yh -v latq,yq -d lonh,xh -d lath,yh -d latq,yq ends_1.nc
ncks -O -d yh,15,15 -d zi,0,0 -v e prog.nc ends_2.nc
ncks -d yh,15,15 -v h -A  prog.nc ends_2.nc
ncks -d yq,15,15 -v v -A  prog.nc ends_2.nc
ncrcat ends_1.nc ends_2.nc ends.nc
#ncatted -a modulo,time,c,c,' ' ends.nc
ncrename -v e,zeta_segment_002 ends.nc
ncrename -v v,v_segment_002 ends.nc
ncrename -v h,dz_v_segment_002 ends.nc

ncks -d yh,15,15 -d zi,0,0 -v e -O  prog.nc ends_3.nc
ncks -d yh,15,15 -v h -A  prog.nc ends_3.nc
ncks -d yq,15,15 -v v -A  prog.nc ends_3.nc
ncrcat -A ends_1.nc ends_3.nc ends.nc
ncrename -v e,zeta_segment_003 ends.nc
ncrename -v v,v_segment_003 ends.nc
ncrename -v h,dz_v_segment_003 ends.nc

ncatted -O -a units,time,m,c,"seconds since 0001-01-01 00:00:00" ends.nc
ncatted -O -a calendar_type,time,a,c,"julian" ends.nc

rm ends_?.nc
