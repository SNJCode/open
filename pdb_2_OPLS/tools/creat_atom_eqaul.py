from biopandas.pdb import PandasPdb
import pprint
import sys
import pandas as pd
if len(sys.argv) < 2:
    print('python creat_rtp_Dename.py equivalent.atoms output.pdb  MOL_52DCCC.itp mm')
    quit()


pdb_data_file=sys.argv[1]
pdb_data_file2=sys.argv[2]
equal_atom_file=sys.argv[3]



data = PandasPdb().read_pdb(pdb_data_file)
het = data.df['HETATM']
pdb_data = het.loc[:, ['atom_number','atom_name','residue_name']]
print(pdb_data[:2])

data2 = PandasPdb().read_pdb(pdb_data_file2)
het2 = data2.df['HETATM']
pdb_data2= het2.loc[:, ['atom_number','atom_name','residue_name']]
print(pdb_data2[:2])


with open(equal_atom_file, "r", encoding='UTF-8')as f:
    res = f.readlines()
atom_list=[ (i.replace('\n','').split(' '))  for i in res ]
print(atom_list)


equal_atom=[]
for i in atom_list:
    if len(i[0]) > 0:
        atom_top=pdb_data[pdb_data['atom_number'] == int(i[0])]
        print(atom_top,i)
        for j in i[1].split(','):
            ser=pdb_data2[pdb_data2['atom_number'] == int(j)]  
            ux=atom_top.values.tolist()[0]
            ux.extend(ser.values.tolist()[0])
            equal_atom.append(ux)

           


equal_atom_df=pd.DataFrame(equal_atom,columns=['Res_atom_number','Res_atom_name','Res','sub_atom_num','sub_atom_name','sub_res'])
#print(equal_atom_df)

import os

file_path = 'atom_eqaul.csv'
try:
    df = pd.read_csv(file_path,index_col=0)
except:
    print("文件为空，创建一个空的 DataFrame")
    df = pd.DataFrame()



df_concatenated = pd.concat([df,equal_atom_df], ignore_index=True)
df_unique = df_concatenated.drop_duplicates(subset=['Res_atom_number','Res_atom_name','Res','sub_atom_num','sub_atom_name','sub_res'])

df_unique .to_csv(file_path)
print(df_unique )



