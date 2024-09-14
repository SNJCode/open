
import numpy as np
#import matplotlib.pyplot as plt
import sys
#导入相关的class
from biopandas.pdb import PandasPdb
import pandas as pd

from Bio.PDB import  PDBIO

ztop_pdb=sys.argv[1]
order_pdb=sys.argv[2]
z1=sys.argv[3]
z2=sys.argv[4]
z3=sys.argv[5]
ord1=sys.argv[6]
ord2=sys.argv[7]
ord3=sys.argv[8]

from Bio.PDB import PDBParser, Superimposer
import sys

parser = PDBParser(QUIET=True)
structure1 = parser.get_structure('structure1', ztop_pdb)
structure2 = parser.get_structure('structure2', order_pdb)
print("len(structure1)",len( [atom.coord for atom in structure1.get_atoms()]  ))
print("len(structure2)",len( [atom.coord for atom in structure2.get_atoms()]  ))

def get_atom_by_serial_number(structure, serial_number):
    """
    根据原子序号获取原子对象
    :param structure: Biopython的结构对象
    :param serial_number: 原子序号
    :return: 对应的原子对象，如果未找到则返回None
    """
    for atom in structure.get_atoms():
        if atom.get_serial_number() == int(serial_number):
            return atom
    return None

atoms1 = [ ] 
atoms2 = [ ]


atoms1.append(get_atom_by_serial_number(structure1, z1))
atoms1.append(get_atom_by_serial_number(structure1, z2))
atoms1.append(get_atom_by_serial_number(structure1, z3))
atoms2.append(get_atom_by_serial_number(structure2, ord1))
atoms2.append(get_atom_by_serial_number(structure2, ord2))
atoms2.append(get_atom_by_serial_number(structure2, ord3))

# 对齐两个结构
super_imposer = Superimposer()
super_imposer.set_atoms(atoms1, atoms2)
super_imposer.apply(structure2.get_atoms())
ros=super_imposer.rotran

structure3 =structure2  #parser.get_structure('structure3', 'aligned_structure2.pdb')

#io = PDBIO()
#io.set_structure(structure3)
#io.save("tran_pdb_file.pdb")

def calculate_distance(atom1, atom2):
    """
    计算两个原子之间的距离。
    :param atom1: 第一个原子对象
    :param atom2: 第二个原子对象
    :return: 两个原子之间的距离（Ångström）
    """
    coord1 = atom1.coord
    coord2 = atom2.coord
    distance = np.linalg.norm(coord1 - coord2)
    return distance

atom_namelist=[]   
resde=[]
for atom in structure1.get_atoms():
    isf=False
    atom_count=0
    isatom=-1
    for atom2 in structure3.get_atoms():
        #distance = atom-atom2
        #print(distance)
        dist=calculate_distance(atom,atom2)
        if dist < 0.2:
            atom_count+=1
            isatom=atom2

    if atom_count == 1:
        atom_namelist.append(isatom.get_id())
        resde.append([atom.get_id(), atom.get_parent().get_resname(), isatom.get_id(), isatom.get_parent().get_resname()])
    else:
        print(atom.get_id(), atom.get_parent().get_resname(), 'False') 
        print('PDB Creat ERROR',atom_count)   
        quit()
        #atom_namelist.append("FF")
        #resde.append([atom.get_id(), atom.get_parent().get_resname(), "FF"])


#读取本地的pdb文件
data = PandasPdb().read_pdb(ztop_pdb)
het=data.df['HETATM']
het['atom_name']=atom_namelist
data.df['HETATM'] = het #修改原data中的df
#print(data.df)
data.to_pdb('test_pdb2gmx.pdb')



file_path = 'pdb_change.csv'
try:
    df = pd.read_csv(file_path,index_col=0)
except:
    df = pd.DataFrame()
inner_df=pd.DataFrame(resde,columns=['ztop_atom','ztop_res','ord_atom','ord_res'])
df_concatenated = pd.concat([df,inner_df], ignore_index=True)
df_unique = df_concatenated.drop_duplicates(subset=['ztop_atom','ztop_res','ord_atom','ord_res'])
df_unique.to_csv(file_path)



