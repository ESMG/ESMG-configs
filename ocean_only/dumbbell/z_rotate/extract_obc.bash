#!/bin/bash
# Extract boundary conditions for the child domain from the output of
# the parent domain.

ncks -O -d yq,40,40 -v vav prog.nc south.nc
ncks -d yh,39,39 -v SSH -A  prog.nc south.nc
ncks -d yh,39,39 -v salt -A  prog.nc south.nc
ncks -d yh,39,39 -v h -A  prog.nc south.nc
ncks -d yh,39,39 -v u -A  prog.nc south.nc
ncatted -a modulo,Time,c,c,' ' south.nc
ncrename -v vav,v_segment_001 south.nc
ncrename -v SSH,zeta_segment_001 south.nc
ncrename -v h,dz_v_segment_001 south.nc
ncks -d yh,39,39 -v h -A  prog.nc south.nc
ncrename -v salt,salt_segment_001 south.nc
ncrename -v u,u_segment_001 south.nc
# Change this if changing DUMBBELL_FRACTION
ncks -d yh,39,39 -v u -A  prog.nc south.nc
ncap2 -A -s 'u(:,:,:,0:1)=0; u(:,:,:,19:20)=0; u(:,:,:,2)=h(:,:,:,2); u(:,:,:,18)=h(:,:,:,17); u(:,:,:,3:17)=0.5*(h(:,:,:,2:16)+h(:,:,:,3:17))' south.nc south.nc
ncrename -v h,dz_salt_segment_001 south.nc
ncrename -v u,dz_u_segment_001 south.nc
ncatted -a units,dz_u_segment_001,m,c,'m' south.nc
## For dvdx
#ncks -d yh,41,41 -v v -A  prog.nc south.nc
#ncrename -v v,dvdx_segment_001 south.nc
#ncap2 -A -s 'dvdx_segment_001(:,:,:,0)=v(:,:,:,42)-v(:,:,:,41)' prog.nc south.nc
#ncks -d yh,41,41 -v v -A  prog.nc south.nc
#ncrename -v v,dz_dvdx_segment_001 south.nc
#ncap2 -A -s 'dz_dvdx_segment_001(:,:,:,:)=dz_v_segment_001(:,:,:,:)' south.nc south.nc

ncks -O -d yq,80,80 -v vav prog.nc north.nc
ncks -d yh,80,80 -v SSH -A  prog.nc north.nc
ncks -d yh,80,80 -v salt -A  prog.nc north.nc
ncks -d yh,80,80 -v h -A  prog.nc north.nc
ncks -d yh,80,80 -v u -A  prog.nc north.nc
ncatted -a modulo,Time,c,c,' ' north.nc
ncrename -v vav,v_segment_002 north.nc
ncrename -v SSH,zeta_segment_002 north.nc
ncrename -v h,dz_v_segment_002 north.nc
ncks -d yh,80,80 -v h -A  prog.nc north.nc
ncrename -v salt,salt_segment_002 north.nc
ncrename -v u,u_segment_002 north.nc
# Change this if changing DUMBBELL_FRACTION
ncks -d yh,80,80 -v u -A  prog.nc north.nc
ncap2 -A -s 'u(:,:,:,0:1)=0; u(:,:,:,19:20)=0; u(:,:,:,2)=h(:,:,:,2); u(:,:,:,18)=h(:,:,:,17); u(:,:,:,3:17)=0.5*(h(:,:,:,2:16)+h(:,:,:,3:17))' north.nc north.nc
ncrename -v h,dz_salt_segment_002 north.nc
ncrename -v u,dz_u_segment_002 north.nc
ncatted -a units,dz_u_segment_002,m,c,'m' north.nc
## For dvdx
#ncks -d yh,81,81 -v v -A  prog.nc north.nc
#ncrename -v v,dvdx_segment_002 north.nc
#ncap2 -A -s 'dvdx_segment_002(:,:,:,0)=v(:,:,:,82)-v(:,:,:,81)' prog.nc north.nc
#ncks -d yh,81,81 -v v -A  prog.nc north.nc
#ncrename -v v,dz_dvdx_segment_002 north.nc
#ncap2 -A -s 'dz_dvdx_segment_002(:,:,:,:)=dz_v_segment_002(:,:,:,:)' north.nc north.nc
