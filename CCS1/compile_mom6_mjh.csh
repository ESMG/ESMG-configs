#!/bin/tcsh -f

source /opt/modules/default/init/tcsh

set MOM6_installdir = /lustre/f1/dev/gfdl_O/Matthew.Harrison/ESMG-configs
set MOM6_rundir = /lustre/f1/dev/gfdl_O/Matthew.Harrison/work

#---------------------------------------------------------------
# use new modules that point to /t1


if (! -d $MOM6_rundir) mkdir $MOM6_rundir
cd $MOM6_rundir;rm -rf *

# Create env file
mkdir -p build/intel/shared/repro/
cat > build/intel/env <<EOF
module use -a /ncrc/home2/fms/local/modulefiles
module unload PrgEnv-intel PrgEnv-pgi PrgEnv-gnu
module unload netcdf fre
module load PrgEnv-intel
module load netcdf/4.3.0
EOF

mkdir -p build/mkmf
ln -fs $MOM6_installdir/src/mkmf/bin build/mkmf/bin
ln -fs $MOM6_installdir/src/mkmf/templates build/mkmf/templates


set compile_fms = 1
set compile_mom = 1


if ( $compile_fms == 1 )  then

   (cd build/intel/shared/repro/; rm -f path_names; \
   $MOM6_rundir/build/mkmf/bin/list_paths $MOM6_installdir/src/FMS; \
   $MOM6_rundir/build/mkmf/bin/mkmf -t $MOM6_rundir/build/mkmf/templates/ncrc-intel.mk -p libfms.a -c "-Duse_libMPI -Duse_netCDF -DSPMD" path_names)

   (cd build/intel/shared/repro/; source ../../env; make NETCDF=3 REPRO=1 libfms.a -j 6)

endif

cd $MOM6_rundir

if ( $compile_mom == 1 ) then

    rm -Rf build/intel/ice_ocean_SIS2/repro/
    mkdir -p build/intel/ice_ocean_SIS2/repro/
    (cd build/intel/ice_ocean_SIS2/repro/; rm -f path_names; \
    $MOM6_rundir/build/mkmf/bin/list_paths ./ $MOM6_installdir/src/MOM6/config_src/{dynamic,coupled_driver} $MOM6_installdir/src/MOM6/src/{*,*/*}/ $MOM6_installdir/src/{atmos_null,coupler,land_null,ice_ocean_extras,icebergs,SIS2,FMS/coupler,FMS/include}/)
    (cd build/intel/ice_ocean_SIS2/repro/; \
   $MOM6_rundir/build/mkmf/bin/mkmf -t $MOM6_rundir/build/mkmf/templates/ncrc-intel.mk -o '-I../../shared/repro' -p 'MOM6 -L../../shared/repro -lfms' -c '-Duse_libMPI -Duse_netCDF -DSPMD -DUSE_LOG_DIAG_FIELD_INFO' path_names )

    (cd build/intel/ice_ocean_SIS2/repro/; source ../../env; make NETCDF=4 REPRO=1 MOM6 -j)

endif

