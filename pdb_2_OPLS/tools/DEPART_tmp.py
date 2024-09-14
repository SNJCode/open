#导入相关的class
from biopandas.pdb import PandasPdb
import pandas as pd
import sys
from itertools import repeat
import pprint
#读取本地的pdb文件
data = PandasPdb().read_pdb(sys.argv[1])
redname_top=sys.argv[2]
atonmae_topx=sys.argv[3]



#pprint.pprint(data.__dict__)
data.df['OTHERS'].loc[1,'record_name']='END'
#print(data.df['OTHERS'])


#print(data.df)

het=data.df['ATOM']

if len(het) ==0 :
  het=data.df['HETATM']
else:
  data.df['HETATM']=data.df['ATOM']
  data.df['ATOM']=pd.DataFrame()


with open("fragment_data.txt", "r", encoding='UTF-8')as f:
    res = f.readlines()

atom_list=[]
for i in res:
  rr=i.split(' ')[1].replace('\n','')
  atom_list.append(rr.split(','))
print(atom_list)

atom_number=len(het['atom_name'])
#print(atom_number)


redisname=[]
redisid=[]
occupancy=[]
b_factor=[]

for i in range(1,atom_number+1):
  for p,j in enumerate(atom_list):
      if str(i) in j:
        redisname.append(redname_top+str(p))
        redisid.append(p+1)
        occupancy.append(1)
        b_factor.append(0)
        break
        
atom_name=[]
for j in het['atom_name']:
   atom_name.append('{}{}'.format(j,atonmae_topx))

#print(redisname)
#print(redisid)


het['atom_name']=atom_name
het['residue_name']=redisname
het['residue_number']=redisid
het['record_name']=list(repeat('HETATM', atom_number))
het['occupancy']=occupancy
het['b_factor']=b_factor



het['element_symbol']=[ '{}'.format(j[0])  for j in het['atom_name'] ]
#het = het['residue_name'].sort_values()
#het= het.sort_values(by='residue_name', ascending=True)


data.df['HETATM'] = het #修改原data中的df
print(data.df)
data.to_pdb('test_res.pdb')
#data.df[jg].to_csv('ouputpdn.csv')
