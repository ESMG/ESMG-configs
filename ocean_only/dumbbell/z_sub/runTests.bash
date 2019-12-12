#!/bin/bash

python parseExp.py

rm input.nml
cp ../common/input.nml .
if [ -f ocean.stats ] ; then
    rm ocean.stats ocean.stats.nc
fi
num=0
while read -r line; do
    PF='MOM_override.'$line
    echo $PF
    if [ ! -d $line ]; then
	mkdir $line
        cp input.nml input.nml.sav
        sed -i -e "/MOM_override/a ,'${PF}'" input.nml
#	diff input.nml input.nml.sav
        mpirun -n 4 ~/src/MOM6/build/symmetric/MOM6 >& output
        mv prog.nc output MOM_parameter_doc.all $line
       	mv input.nml.sav input.nml
	python skill.py $num
    fi
    ((num++))
done < Codes.txt
echo('num=',num)
rm input.nml
ln -s ../common/input.nml .
