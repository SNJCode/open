cd run 

cp ../tools/gmx_file/* ./

pp=$(pwd)
./3_packmol.sh PSC 10

cd $pp
 ./4_min.sh  
 
 cd $pp
 ./5_min_cg.sh 
 
 cd $pp
./6_th.sh  

cd $pp
./7npt.sh 

cd $pp
./8npt.sh  


cd $pp
./9npt.sh

