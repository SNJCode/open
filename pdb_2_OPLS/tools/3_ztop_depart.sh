#conda activate ztop

if [ "$#" -lt 2 ]; then
    echo " log A "
    exit
 
 fi
 
ff=$1
folder=$(echo ${ff%/*} | sed 's/\///g' | sed 's/\.//g' )

name=${ff#*/} 
name=${name%.*}


cur=$(pwd)
ztop_path=$(cat $cur/tools/ztop_path | sed -n '1p')
res=$(cat $folder/depart/resname | sed -n '1p' )

echo $ztop_path $res $name $folder
pdb_folder=$cur/$folder/pdb



cd $ztop_path

cp $cur/${folder}/${name}*  ./

python3  ztop.py -g ""$name".log" -o $name.top,$name.gro



IFS=' ' read -r -a myArray <<< $(cat $cur/${folder}/depart/fragment_input.txt | sed -n '1p')


length=${#myArray[@]}
echo myArray_length:$length

icc=0
fragnm=""
resindex=0
ZIMU=(A B C D E F G H I J K L M N O P Q R S T U V W Y Z )

frag=$(echo ${ZIMU[@]} | sed 's/ /\n/g' | grep -n $2 | awk -F : '{print $1-1}' )

for element in "${myArray[@]}"; do
  echo "Element: $element"
done

while  [ $icc -lt $length ]
do
	
     icc=$((icc+1))
     if [ $icc -eq 1 ];then
     	#echo  ${myArray[0]}  ${myArray[1]} 
     	 python3 ztop.py -f ""${ZIMU[$frag]}";p="${name}".top;x="${name}".gro;site="${ZIMU[$frag]}"1:"${myArray[0]}"-"${myArray[1]}";resname=""${res}${resindex}"";comment="${res}${resindex}"" --savelib 
     	fragnm=${fragnm}${ZIMU[$frag]}
     	
     	echo python3 ztop.py -f ""${ZIMU[$frag]}";p="${name}".top;x="${name}".gro;site="${ZIMU[$frag]}"1:"${myArray[0]}"-"${myArray[1]}";resname=""${res}${resindex}"";comment="${res}${resindex}"" --savelib 

     elif [ $icc -eq $length ];then 
     	left1=$(($icc-1))
     	left2=$(($icc-2))
     	#echo llll
     	#echo  ${myArray[$left1]}     ${myArray[$left2]} 
     	 python3 ztop.py -f ""${ZIMU[frag]}";p="${name}".top;x="${name}".gro;site="${ZIMU[$frag]}"1:"${myArray[$left1]}"-"${myArray[$left2]}";resname=""${res}${resindex}"";comment="${res}${resindex}"" --savelib      
     	     
     	 echo   	 python3 ztop.py -f ""${ZIMU[frag]}";p="${name}".top;x="${name}".gro;site="${ZIMU[$frag]}"1:"${myArray[$left1]}"-"${myArray[$left2]}";resname=""${res}${resindex}"";comment="${res}${resindex}"" --savelib      
     	 
     	fragnm=${fragnm}${ZIMU[$frag]}
     	break
     else 
     	left1=$(($icc-1))
     	left2=$(($icc-2))
     	right1=$(($icc))
     	right2=$(($icc+1))
     	icc=$((icc+1))
     	 frag2=$((frag+1))
     	#echo  ${myArray[$left1]}     ${myArray[$left2]}     ${myArray[$right1]}     ${myArray[$right2]}  
     	 python3 ztop.py -f ""${ZIMU[frag]}";p="${name}".top;x="${name}".gro;site="${ZIMU[$frag]}"1:"${myArray[$left1]}"-"${myArray[$left2]}",""${ZIMU[$frag2]}"1:"${myArray[right1]}"-"${myArray[$right2]}"";resname=""${res}${resindex}"";comment="${res}${resindex}"" --savelib 
     	  
     	 echo  python3 ztop.py -f ""${ZIMU[frag]}";p="${name}".top;x="${name}".gro;site="${ZIMU[$frag]}"1:"${myArray[$left1]}"-"${myArray[$left2]}",""${ZIMU[$frag]}"1:"${myArray[right1]}"-"${myArray[$right2]}"";resname=""${res}${resindex}"";comment="${res}${resindex}"" --savelib 
     	 
    	fragnm=${fragnm}${ZIMU[$frag]}
     	frag=$((frag+1))
     fi
 frag=$((frag+1))
 resindex=$((resindex+1))
done


 python3 ztop.py --loadlib -b $fragnm  -o FRAG.pdb
 echo  python3 ztop.py --loadlib -b $fragnm  -o FRAG.pdb

cp FRAG.pdb $pdb_folder

#cp FRAG.pdb ${cur}

##############
#python ztop.py -g "mi.log" -o mi.top,mi.gro

#python ztop.py -f "M;p=mi.top;x=mi.gro;site=A1:9-45,B1:7-40;resname=MI1;comment=MI1" --savelib

#python ztop.py -f "L;p=mi.top;x=mi.gro;site=L1:45-9;resname=MI0;comment=MI0" --savelib

#python ztop.py -f "R;p=mi.top;x=mi.gro;site=R1:40-7;resname=MI2;comment=MI2" --savelib




