

ztop=$(conda info --envs  | grep '\*' | awk '{print $1}' )
if [ "$ztop" != "ztop" ];then

echo conda activate ztop 
exit
fi



top_path=$(pwd)
./tools/1_depart_noorder.sh oh/MOL_0BC5E4.pdb  oh/frag2.txt 

cd $top_path
./tools/2_crete_res.sh oh OH


cd $top_path
./tools/3_ztop_depart.sh oh/oh.log E




cd $top_path
./tools/4_insert_equal_atom.sh test_res_ps.pdb test_res_oh.pdb oh/atom_oh.txt 


cd $top_path
./tools/5_itp.sh oh/MOL_0BC5E4.itp 


cd $top_path
./tools/6_install.sh oh

cd $top_path
./tools/7_pdb_atom_map.sh oh  


