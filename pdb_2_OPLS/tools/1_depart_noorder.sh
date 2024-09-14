

if [ "$#" -lt 2 ]; then
    echo " pdb atomfile "
    exit
 
 fi
 

pw=$(pwd)

ff=$1
folder=$(echo ${ff%/*} | sed 's/\///g' | sed 's/\.//g' )
echo $folder


cd $folder

mkdir  depart

cd depart

cp ${pw}/$1 ./ligpargen.pdb
cp ${pw}/$2 ./frag.txt

cp ${pw}/tools/depart.vmd  ./
cp ${pw}/tools/depart_noorder.sh  ./


 
./depart_noorder.sh  ligpargen.pdb  $(cat frag.txt | sed -n '1p' )

