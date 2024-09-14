

mkdir pdb_atom_map
cd pdb_atom_map

cp ../tools/creat_tran_by_two.py ./
cp ../tools/crete_trans_file.py ./

mol=$1
mol=$(echo $mol | sed 's/\///g')


python3 creat_tran_by_two.py  ../$mol/pdb/FRAG.pdb  ../$mol/pdb/order.pdb


