

if [ "$#" -lt 2 ]; then
    echo "pdbfrag_name pdbfile "
    exit
 
 fi
 

ff='run'
mkdir $ff

fol=$(pwd)/${ff}

pp=$(cat ./tools/ztop_path | sed -n '1p')


cd $pp

python3 ztop.py --loadlib -b $1  -o $fol/$2.pdb




