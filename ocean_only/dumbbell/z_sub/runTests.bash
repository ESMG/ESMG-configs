#!/bin/bash

python parseExp.py

rm input.nml
cp ../common/input.nml .
if [ -f ocean.stats ] ; then
    rm ocean.stats ocean.stats.nc
fi

while read -r line; do
    PF='MOM_override.'$line
    if [ ! -d $line ]; then
	mkdir $line
        cp input.nml input.nml.sav
        sed -i -e "/MOM_override/a ,'${PF}'" input.nml
#	diff input.nml input.nml.sav
        mpirun -np 4 /center1/AKWATERS/kshedstrom/MOM6/build/gnu/symmetric_ocean_only/repro/MOM6 >& output
        mv prog.nc output MOM_parameter_doc.all $line
       	mv input.nml.sav input.nml
    fi
done < Codes.txt

rm input.nml
ln -s ../common/input.nml .
