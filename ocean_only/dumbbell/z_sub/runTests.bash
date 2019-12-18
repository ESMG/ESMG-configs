#!/bin/bash

python parseExp.py

rm input.nml
cp ../common/input.nml .
if [ -f ocean.stats ] ; then
    rm ocean.stats ocean.stats.nc
fi

expList=''
while read -r line; do
    expList="$expList $line"
done < <(cat Codes.txt)


 for exp in $expList; do
     pf='MOM_override'.$exp
     echo $pf
     if [ ! -d $exp ]; then
 	mkdir $exp
        cp input.nml input.nml.sav
        sed -i -e "/MOM_override/a ,'${pf}'" input.nml
        mpirun -n 4 ~/src/MOM6/build/symmetric/MOM6 >& output;
        mv prog.nc output MOM_parameter_doc.all ocean.stats* $exp
        mv input.nml.sav input.nml
 	python rms_errors.py $exp
     fi
 done

rm input.nml
ln -s ../common/input.nml .
