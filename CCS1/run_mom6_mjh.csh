#!/bin/tcsh -f

source /opt/modules/default/init/tcsh

set MOM6_installdir = /lustre/f1/dev/gfdl_O/Matthew.Harrison/ESMG-configs
set MOM6_rundir = /lustre/f1/dev/gfdl_O/Matthew.Harrison/work

#---------------------------------------------------------------
# use new modules that point to /t1


if (! -d $MOM6_rundir) mkdir $MOM6_rundir
cd $MOM6_rundir

set execfile = '$MOM6_rundir/build/intel/ice_ocean_SIS2/repro/MOM6'

set workdir = `date +%G%m%d%H%M`
mkdir $workdir
cd $workdir
cp -r $MOM6_installdir/CCS1 .

aprun -n 1 $execfile


