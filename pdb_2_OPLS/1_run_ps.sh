

ztop=$(conda info --envs  | grep '\*' | awk '{print $1}' )
if [ "$ztop" != "ztop" ];then

echo conda activate ztop 
exit
fi



top_path=$(pwd)
./tools/1_depart_noorder.sh ./ps/MOL_23525C.pdb  ./ps/frag.txt  #pdb_file frag_file

cd $top_path
./tools/2_crete_res.sh 'ps' PS #frag_folder resname

#vmd test_res_ps.pdb -e tools/resname_vmd 
#############
# conda activate ztop 
cd $top_path
./tools/3_ztop_depart.sh ps/ph.log A   #Gaussain_file resIndex



cd $top_path
./tools/4_insert_equal_atom.sh  test_res_ps.pdb test_res_ps.pdb ps/atom.txt 

####creat_res.pdb atom.txt 

cd $top_path
./tools/5_itp.sh ps/MOL_23525C.itp 


cd $top_path
./tools/6_install.sh 'ps'

cd $top_path
./tools/7_pdb_atom_map.sh 'ps'  


