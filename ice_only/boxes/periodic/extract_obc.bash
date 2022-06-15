#!/bin/bash
# Extract boundary conditions for the child domain from the output of
# the parent domain. Run this before extract_obc.py.

# West
ncks -O -d xB,5,5 -d yT,5,14  -v uice 10000101.daily.nc west.nc
ncks -d xT,4,4 -d yT,5,14 -v vice -A  10000101.daily.nc west.nc
ncks -d xT,4,4 -d yT,5,14 -v siconc -A  10000101.daily.nc west.nc
ncks -d xT,4,4 -d yT,5,14 -v hice -A  10000101.daily.nc west.nc
ncks -d xT,4,4 -d yT,5,14 -v str_d -A  10000101.daily.nc west.nc
ncks -d xT,4,4 -d yT,5,14 -v str_t -A  10000101.daily.nc west.nc
ncks -d xB,5,5 -d yB,5,15 -v str_s -A  10000101.daily.nc west.nc
ncatted -a modulo,time,c,c,' ' west.nc
ncrename -v uice,ui_segment_001 west.nc
ncrename -v vice,vi_segment_001 west.nc
ncrename -v siconc,ci_segment_001 west.nc
ncrename -v hice,hi_u_segment_001 west.nc
ncrename -v str_d,str_d_segment_001 west.nc
ncrename -v str_t,str_t_segment_001 west.nc
ncrename -v str_s,str_s_segment_001 west.nc

# East
ncks -O -d xB,15,15 -d yT,5,14 -v uice 10000101.daily.nc east.nc
ncks -d xT,15,15 -d yT,5,14 -v vice -A  10000101.daily.nc east.nc
ncks -d xT,15,15 -d yT,5,14 -v siconc -A  10000101.daily.nc east.nc
ncks -d xT,15,15 -d yT,5,14 -v hice -A  10000101.daily.nc east.nc
ncks -d xT,15,15 -d yT,5,14 -v str_d -A  10000101.daily.nc east.nc
ncks -d xT,15,15 -d yT,5,14 -v str_t -A  10000101.daily.nc east.nc
ncks -d xB,15,15 -d yB,5,15 -v str_s -A  10000101.daily.nc east.nc
ncatted -a modulo,time,c,c,' ' east.nc
ncrename -v uice,ui_segment_002 east.nc
ncrename -v vice,vi_segment_002 east.nc
ncrename -v siconc,ci_segment_002 east.nc
ncrename -v hice,hi_segment_002 east.nc
ncrename -v str_d,str_d_segment_002 east.nc
ncrename -v str_t,str_t_segment_002 east.nc
ncrename -v str_s,str_s_segment_002 east.nc

# North
ncks -O -d xT,5,14 -d yB,15,15 -v uice 10000101.daily.nc north.nc
ncks -d xT,5,14 -d yT,15,15 -v vice -A  10000101.daily.nc north.nc
ncks -d xT,5,14 -d yT,15,15 -v siconc -A  10000101.daily.nc north.nc
ncks -d xT,5,14 -d yT,15,15 -v hice -A  10000101.daily.nc north.nc
ncks -d xT,5,14 -d yT,15,15 -v str_d -A  10000101.daily.nc north.nc
ncks -d xT,5,14 -d yT,15,15 -v str_t -A  10000101.daily.nc north.nc
ncks -d xB,5,15 -d yB,15,15 -v str_s -A  10000101.daily.nc north.nc
ncatted -a modulo,time,c,c,' ' north.nc
ncrename -v uice,ui_segment_003 north.nc
ncrename -v vice,vi_segment_003 north.nc
ncrename -v siconc,ci_segment_003 north.nc
ncrename -v hice,hi_segment_003 north.nc
ncrename -v str_d,str_d_segment_003 north.nc
ncrename -v str_t,str_t_segment_003 north.nc
ncrename -v str_s,str_s_segment_003 north.nc

# South
ncks -O -d xT,5,14 -d yB,5,5 -v uice 10000101.daily.nc south.nc
ncks -d xT,5,14 -d yT,4,4 -v vice -A  10000101.daily.nc south.nc
ncks -d xT,5,14 -d yT,4,4 -v siconc -A  10000101.daily.nc south.nc
ncks -d xT,5,14 -d yT,4,4 -v hice -A  10000101.daily.nc south.nc
ncks -d xT,5,14 -d yT,4,4 -v str_d -A  10000101.daily.nc south.nc
ncks -d xT,5,14 -d yT,4,4 -v str_t -A  10000101.daily.nc south.nc
ncks -d xB,5,15 -d yB,4,4 -v str_s -A  10000101.daily.nc south.nc
ncatted -a modulo,time,c,c,' ' south.nc
ncrename -v uice,ui_segment_004 south.nc
ncrename -v vice,vi_segment_004 south.nc
ncrename -v siconc,ci_segment_004 south.nc
ncrename -v hice,hi_segment_004 south.nc
ncrename -v str_d,str_d_segment_004 south.nc
ncrename -v str_t,str_t_segment_004 south.nc
ncrename -v str_s,str_s_segment_004 south.nc
