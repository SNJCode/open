#导入相关的class
from biopandas.pdb import PandasPdb
import pandas as pd
import sys
from itertools import repeat
import pprint
#读取本地的pdb文件
data= PandasPdb().read_pdb(sys.argv[1])


het=data.df['HETATM']
pdb_data = het.loc[:, ['atom_number','atom_name','residue_name']]



            #index_to_delete = pdb_data [pdb_data ['atom_number'] == int(j)].index
            #pdb_data = pdb_data.drop(index_to_delete)

try:
    equal_atom_df=pd.read_csv(sys.argv[2])
except:
    equal_atom_df = pd.DataFrame()
    

print(equal_atom_df)

def change_atom(a):
    if equal_atom_df.empty:
       return a
    issub=equal_atom_df[equal_atom_df['sub_atom_name']== a]
    if issub.empty:
        return a
    else:
        return issub['Res_atom_name'].to_list()[0]
    

het['atom_name']=het['atom_name'].apply(change_atom)
#het= het.groupby('residue_name').apply(lambda x: x.sort_values('atom_name')).reset_index(drop=True)
het= het.sort_values(by='residue_name', ascending=True)

lenx=len(het['residue_name'])
het['atom_number']=[i for i in range(1,lenx+1)]
het['line_idx']=[i for i in range(1,lenx+1)]

data.df['HETATM'] = het #修改原data中的df
#data.df['HETATM'].to_csv('111.csv')
data.to_pdb('order.pdb')

