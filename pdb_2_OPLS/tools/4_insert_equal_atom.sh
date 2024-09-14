
#!/bin/bash

# 检查参数数量
if [ "$#" -lt 3 ]; then
    echo "parm is " PDB PDB EQUAL
    exit
fi



mkdir insert_equal_atom


cd insert_equal_atom
cp ../tools/creat_atom_eqaul.py  ./
cp ../$1 ./
cp ../$2 ./
cp ../$3 ./


ff=$1
name=${ff#*/} 

ff=$2
name2=${ff#*/} 

ff=$3
atom=${ff#*/} 

echo $name $name2 $atom

python3 creat_atom_eqaul.py $name $name2 $atom



