#导入相关的class
from biopandas.pdb import PandasPdb
import pandas as pd
import sys
from itertools import repeat
import pprint

#读取本地的pdb文件
data = PandasPdb().read_pdb(sys.argv[1])
het=data.df['HETATM']

res_data=pd.read_csv('pdb_change.csv')



#['ztop_atom','ztop_res','ord_atom','ord_res']
def modify_row(row):
    res_name=row['residue_name'] 
    atom_name= row['atom_name'] 
    after_df=res_data[(res_data['ztop_atom'] ==  atom_name) & (res_data['ztop_res'] == res_name)]
    
    
    row.loc['residue_name']= after_df['ord_res'].iat[0]
    row.loc['atom_name']= after_df['ord_atom'].iat[0]
    return row



    
het=het.apply(modify_row, axis=1)
    



data.df['HETATM'] = het #修改原data中的df
data.to_pdb('output.pdb')
#data.df[jg].to_csv('ouputpdn.csv')
