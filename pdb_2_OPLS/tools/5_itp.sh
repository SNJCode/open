
#!/bin/bash

# 检查参数数量
if [ "$#" -lt 1  ]; then
    echo "itp " 
    exit
fi


ff=$1
##name=${ff#*/} 
folder=$(echo ${ff%/*} | sed 's/\///g' | sed 's/\.//g' )
#name=${name%.*}

cd $folder

mkdir creat_itp
cd creat_itp


cp ../../tools/creat_rtp_Dename.py  ./
cp ../../tools/order_by_pdb.py ./
cp ../../insert_equal_atom/atom_eqaul.csv ./
cp ../../$1 ./mol.itp

kk=$(cat ../depart/resname | sed -n '1p')


python3 creat_rtp_Dename.py atom_eqaul.csv  ../../test_res_${folder}.pdb mol.itp  ${kk:0:1}


python3 order_by_pdb.py ../../test_res_${folder}.pdb  atom_eqaul.csv 
cat order.pdb |  sed -n '/REMARK/,/END/p'  > ../pdb/order.pdb


