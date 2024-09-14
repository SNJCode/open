
if [ "$#" -lt 2 ]; then
    echo " folder resname "
    exit
 
 fi
 

cd $1


mkdir pdb
cd depart

echo $2 > resname

ResName=$(cat resname | sed -n '1p' )
ResTop=${ResName:0:1}


cp ../../tools/DEPART_tmp.py  ./


python DEPART_tmp.py ligpargen.pdb  $ResName $ResTop
cp test_res.pdb ../../test_res_$1.pdb
