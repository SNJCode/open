name=$@
echo $name 
filename=$1
arg=$(echo $name | awk '{ $1="";print $0}')


echo $arg > fragment_input.txt

echo "mol new ${filename}
source depart.vmd
get_part ${arg}" > a.txt


vmd < a.txt | tee  b.out 
rm fragment_data.txt fragment_name.txt
cat b.out | grep A, | sed 's/A,//g' | awk '{printf("frag%d %s\n",NR,$0)}' > fragment_data.txt
rm a.txt b.out 






