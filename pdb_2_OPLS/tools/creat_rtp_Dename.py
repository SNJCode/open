from biopandas.pdb import PandasPdb
import pprint
import sys
import pandas as pd
if len(sys.argv) < 2:
    print('python creat_rtp_Dename.py equivalent.atoms output.pdb  MOL_52DCCC.itp mm')
    quit()

equal_atom_file=sys.argv[1]
pdb_data_file=sys.argv[2]
itp_data_file=sys.argv[3]
atomtopx=sys.argv[4]

import os
os.system('mkdir pdb2data')

data = PandasPdb().read_pdb(pdb_data_file)
het = data.df['HETATM']
pdb_data = het.loc[:, ['atom_number','atom_name','residue_name']]

###############################################################   pdb2data/residuetypes.dat
dict = {}
res_data='pdb2data/residuetypes.dat'
if  os.path.exists(res_data):
    with open(res_data, 'r') as file:
        for line in file:
            key, value = line.strip().split(' ')
            dict[key] = value

for j in set(het.loc[:, 'residue_name'].tolist()):
        dict[j]='Protein'

with open(res_data, 'w') as f:
    for key, value in dict.items():
        f.write(f'{key} {value}\n')
############################################################### read_itp
import re
itp_data=[]
with open(itp_data_file,"r") as f:
    for line in f.readlines():
        itp_data.append(line.strip('\n'))

itp_data.append('ENDNEND')
itp_atoms_dict_list = {}
itp_temp=[]
globax=''
current_items=''
for i in itp_data:
    if ';' in i:
        continue
    if 'ENDNEND' in i:
        itp_atoms_dict_list[current_items]=itp_temp
        break
    m=re.match('(\s*)\[(\s)*(\w*)(\s)*\](\s)*',i)
    if m:  
        if len(itp_temp) > 0:
            itp_atoms_dict_list[current_items]=itp_temp  

        if globax == 'dihedralsimp' and m.groups()[2]== 'dihedrals':
            current_items='dihedrals'

        elif m.groups()[2]== 'dihedrals':
            globax='dihedralsimp'
            current_items='impropers'
        else:
            current_items=m.groups()[2]

        itp_temp=[]
        
    elif current_items!='' and i.strip() !='':
        itp_temp.append(i.split())

#pprint.pprint(itp_atoms_dict_list )
#xp('----------------atoms---------------------------')
itp_atoms=itp_atoms_dict_list['atoms']
itp_atoms_df=pd.DataFrame(itp_atoms,columns=[ 'nr','atomstype','resnr','residue','atom_name' ,'cgnr' ,'charge' ,'mass'  ])
itp_atoms_df['atom_name'] = itp_atoms_df['atom_name'].apply(lambda x: '{}{}'.format(x,atomtopx))
itp_atoms_df['atomstype'] = itp_atoms_df['atomstype'].apply(lambda x: '{}{}'.format(x,atomtopx))
print(itp_atoms_df[:2],'\n')

#xp('----------------bonds---------------------------')
itp_bonds=itp_atoms_dict_list['bonds']
itp_bonds_df=pd.DataFrame(itp_bonds,columns=[ 'atom1','atom2','xxxx','num1','num2'   ])

def change_atom_name(a):
    xx=itp_atoms_df[itp_atoms_df['nr'] == a].loc[:,"atom_name"].tolist()
    if len(xx) == 1:       
            return xx[0]
    else:
        return 'ERROR'+str(a)
 
itp_bonds_df["atom1"]=itp_bonds_df["atom1"].apply(change_atom_name)
itp_bonds_df["atom2"]=itp_bonds_df["atom2"].apply(change_atom_name)
print(itp_bonds_df[:2],'\n')

#xp('----------------angle---------------------------')
itp_angles =itp_atoms_dict_list['angles']
itp_angles_df=pd.DataFrame(itp_angles ,columns=[ 'atom1','atom2','atom3','funct','c0'  ,'c1'  ])
itp_angles_df["atom1"]=itp_angles_df["atom1"].apply(change_atom_name)
itp_angles_df["atom2"]=itp_angles_df["atom2"].apply(change_atom_name)
itp_angles_df["atom3"]=itp_angles_df["atom3"].apply(change_atom_name)
print(itp_angles_df[:2],'\n')

#xp('----------------dihedrals---------------------------')
itp_dihedrals =itp_atoms_dict_list['dihedrals']
itp_dihedrals_df=pd.DataFrame(itp_dihedrals ,columns=[ 'atom1','atom2','atom3','atom4','funct','c0'  ,'c1'  ,'c2','c3','c4','c5' ])
itp_dihedrals_df["atom1"]=itp_dihedrals_df["atom1"].apply(change_atom_name)
itp_dihedrals_df["atom2"]=itp_dihedrals_df["atom2"].apply(change_atom_name)
itp_dihedrals_df["atom3"]=itp_dihedrals_df["atom3"].apply(change_atom_name)
itp_dihedrals_df["atom4"]=itp_dihedrals_df["atom4"].apply(change_atom_name)
print(itp_dihedrals_df[:2],'\n')


#xp('----------------impropers--------------------------')
if 'impropers' in itp_atoms_dict_list:
    itp_impropers =itp_atoms_dict_list['impropers']
    itp_impropers_df=pd.DataFrame(itp_impropers,columns=[ 'atom1','atom2','atom3','atom4','funct','c0'  ,'c1'  ,'c2' ])
    itp_impropers_df["atom1"]=itp_impropers_df["atom1"].apply(change_atom_name)
    itp_impropers_df["atom2"]=itp_impropers_df["atom2"].apply(change_atom_name)
    itp_impropers_df["atom3"]=itp_impropers_df["atom3"].apply(change_atom_name)
    itp_impropers_df["atom4"]=itp_impropers_df["atom4"].apply(change_atom_name)

    print(itp_impropers_df[:2],'\n')
    
    print('--------------------------------------------------------------\n')
else:
    itp_impropers_df = None



############################################################# equal_atom_pandas_creat

#xp('----------------atomtypes---------------------------')

itp_atomtype =itp_atoms_dict_list['atomtypes']
itp_atomtype_df=pd.DataFrame(itp_atomtype,columns=['atomstype','atom_name','atom_mass','char','xxx','par1','par2'])
itp_atomtype_df['atomstype'] = itp_atomtype_df['atomstype'].apply(lambda x: '{}{}'.format(x,atomtopx))
itp_atomtype_df['atom_name'] = itp_atomtype_df['atom_name'].apply(lambda x: '{}{}'.format(x,atomtopx))
print(itp_atomtype_df[:2],'\n')
#############################################################

frag_list = []
resname=list(set(pdb_data.loc[:,'residue_name'].tolist()))
resname.sort()
print('pdb_resname',resname)

for res in resname:
    resl = pdb_data[pdb_data['residue_name']== res].loc[:,'atom_name'].tolist()
    frag_list.append(resl)
########################################

print('------------fragment_data---------')
print(frag_list,'\n')

###########################
########################################################
try:
    equal_atom_df=pd.read_csv(equal_atom_file,index_col=0)
except:
    equal_atom_df = pd.DataFrame()
    

print(equal_atom_df)

def atom_change(a):
    x=a['atom_name']
    if equal_atom_df.empty:
       return a
    issub=equal_atom_df[equal_atom_df['sub_atom_name']== x]
    if issub.empty:
        return a
    else:
        rtx=issub['Res_atom_name'].to_list()[0]    
        a.loc['atom_name']= rtx
        return a
    
def atom_name_change(a):
    if equal_atom_df.empty:
       return a
    issub=equal_atom_df[equal_atom_df['sub_atom_name']== a]
    if issub.empty:
        return a
    else:
        return issub['Res_atom_name'].to_list()[0]

def frag_match(a,b):
    if b == 0:
        if a in frag_list[1]:
            return '+'+atom_name_change(a)   
    elif b==len(frag_list)-1 :
        if a in frag_list[-2]:
            return '-'+atom_name_change(a)
    else:
        if a in frag_list[b-1]:
            return '-'+atom_name_change(a)
        elif a in frag_list[b+1]:
            return '+'+atom_name_change(a)
    return atom_name_change(a)

################################################################
print('#'*50)
print('#'*50)

for ifrag in range(len(frag_list)):
    
#      nr  atomstype resnr residue atom_name cgnr   charge     mass
#0  1  Mopls_800     1     MOL      MC00    1  -0.1343  12.0110
#1  2  Mopls_801     1     MOL      MC01    1  -0.0774  12.0110 
    atomlist=itp_atoms_df[itp_atoms_df['atom_name'].isin(frag_list[ifrag]) ]
    atomlist= atomlist.apply(atom_change,axis=1)
    name=resname[ifrag]

    dd=itp_bonds_df[itp_bonds_df['atom1'].isin(frag_list[ifrag]) |  itp_bonds_df['atom2'].isin(frag_list[ifrag])]
    df_rtp_bond=dd.loc[:,["atom1","atom2","num1","num2"]].copy()
    df_rtp_bond["atom1"]=df_rtp_bond["atom1"].apply(frag_match,args=(ifrag ,))
    df_rtp_bond["atom2"]=df_rtp_bond["atom2"].apply(frag_match,args=(ifrag ,))
    #print(df_rtp_bond[:2],'\n')
 
    dd=itp_angles_df[itp_angles_df['atom1'].isin(frag_list[ifrag]) |  itp_angles_df['atom2'].isin(frag_list[ifrag]) |  itp_angles_df['atom3'].isin(frag_list[ifrag]) ]
    df_rtp_angle=dd.loc[:,['atom1','atom2','atom3','c0'  ,'c1']].copy()
    df_rtp_angle["atom1"]=df_rtp_angle["atom1"].apply(frag_match,args=(ifrag ,))
    df_rtp_angle["atom2"]=df_rtp_angle["atom2"].apply(frag_match,args=(ifrag ,))
    df_rtp_angle["atom3"]=df_rtp_angle["atom3"].apply(frag_match,args=(ifrag ,))
    #print(df_rtp_angle[:2],'\n')

    dd=itp_dihedrals_df[itp_dihedrals_df['atom1'].isin(frag_list[ifrag]) |  itp_dihedrals_df['atom2'].isin(frag_list[ifrag]) | itp_dihedrals_df['atom3'].isin(frag_list[ifrag]) | itp_dihedrals_df['atom4'].isin(frag_list[ifrag]) ]
    df_rtp_diheadras=dd.loc[:,['atom1','atom2','atom3','atom4','c0','c1','c2','c3','c4','c5']].copy()
    df_rtp_diheadras["atom1"]=df_rtp_diheadras["atom1"].apply(frag_match,args=(ifrag ,))
    df_rtp_diheadras["atom2"]=df_rtp_diheadras["atom2"].apply(frag_match,args=(ifrag ,))
    df_rtp_diheadras["atom3"]=df_rtp_diheadras["atom3"].apply(frag_match,args=(ifrag ,))
    df_rtp_diheadras["atom4"]=df_rtp_diheadras["atom4"].apply(frag_match,args=(ifrag ,))
    #print(df_rtp_diheadras[:2],'\n')
 
    if itp_impropers_df is not None:
        dd=itp_impropers_df[itp_impropers_df['atom1'].isin(frag_list[ifrag]) |  itp_impropers_df['atom2'].isin(frag_list[ifrag]) | itp_impropers_df['atom3'].isin(frag_list[ifrag]) | itp_impropers_df['atom4'].isin(frag_list[ifrag]) ]
        df_rtp_impropers=dd.loc[:,['atom1','atom2','atom3','atom4','c0','c1','c2']].copy()
        df_rtp_impropers["atom1"]=df_rtp_impropers["atom1"].apply(frag_match,args=(ifrag ,))
        df_rtp_impropers["atom2"]=df_rtp_impropers["atom2"].apply(frag_match,args=(ifrag ,))
        df_rtp_impropers["atom3"]=df_rtp_impropers["atom3"].apply(frag_match,args=(ifrag ,))
        df_rtp_impropers["atom4"]=df_rtp_impropers["atom4"].apply(frag_match,args=(ifrag ,))
        #print(df_rtp_impropers[:2],'\n')
    else:
        df_rtp_impropers=None
  

    with open('pdb2data/{}.rtp'.format(name), 'w') as f:
        f.write('[ bondedtypes ]\n; bonds  angles  dihedrals  impropers all_dihedrals nrexcl HH14 RemoveDih\n1       1          3          1        1         3      1     0\n')
        f.write(' [{}] \n\n'.format(name))
        f.write(' [atoms] \n'.format(ifrag))

        sx=atomlist.loc[:,['atom_name','atomstype','charge']]
        for index, row in sx.iterrows():
                f.write('{} {} {} 0\n'.format(row['atom_name'],row['atomstype'],row['charge']               ))
        f.write('\n')
    
        f.write(' [bonds] \n'.format(ifrag))
        for index, row in df_rtp_bond.iterrows():
            #print(row["atom1"],row["atom2"],row["num1"],row["num2"], file=f)
            f.write('{} {} {} {}\n'.format(row["atom1"],row["atom2"],row["num1"],row["num2"]  ))
        f.write('\n')

        f.write(' [angles] \n'.format(ifrag))
        for index, row in df_rtp_angle.iterrows():
            #print(row["atom1"],row["atom2"],row["atom3"],row["c0"],row["c1"] ,file=f)  
            f.write('{} {} {} {}  {} \n'.format(row["atom1"],row["atom2"],row["atom3"],row["c0"],row["c1"] ))

        f.write('\n')

       
        if df_rtp_impropers is not None:
            f.write(' [ impropers ] \n'.format(ifrag))
            for index, row in df_rtp_impropers.iterrows():
                #print(row["atom1"],row["atom2"],row["atom3"],row["atom4"],row["c0"],row["c1"] ,file=f)  
                f.write('{} {} {} {} {} {} {} \n'.format(row["atom1"],row["atom2"],row["atom3"],row["atom4"],row["c0"],row["c1"],row["c2"]))
            f.write('\n')

        f.write(' [dihedrals ] \n'.format(ifrag))
        for index, row in df_rtp_diheadras.iterrows():
            #print(row["atom1"],row["atom2"],row["atom3"],row["atom4"],row["c0"],row["c1"],row["c2"] ,file=f) 
            f.write('{} {} {} {} {} {} {} {} {} {} \n'.format(row["atom1"],row["atom2"],row["atom3"],row["atom4"],row["c0"],row["c1"],row["c2"],row["c3"],row["c4"],row["c5"] ))

        f.write('\n')

    
    
   

################################################atoms


dict = {}
res_data='pdb2data/atomtypes.atp'
if  os.path.exists(res_data):
    with open(res_data, 'r') as file:
        for line in file:
            key, value = line.strip().split(' ')
            dict[key.strip()] = value

for index, row in itp_atomtype_df.loc[:,['atomstype','atom_mass']].iterrows():
        dict[row["atomstype"]]=row["atom_mass"]

with open(res_data, 'w') as f:
    for key, value in dict.items():
        f.write(f'{key.strip()} {value}\n')



############################


def mass_to_ele(a):
    if a[0] == 'C':
        return '6'
    elif a[0] == 'O':
        return '8'
    elif a[0] == 'N':
        return '7'
    elif a[0] == 'H':
        return '1'
    elif a[0] == 'F':
        return '9'
    elif a[0] == 'S':
        return '16'
    elif a[0] == 'P':
        return '15'    

print('---------------------------inner_df[:2]-------------------------------------------------------------------------------------')
inner_df=pd.merge(itp_atomtype_df,itp_atoms_df,how='inner',on='atomstype')
inner_df["atom_ele"]=inner_df["atom_name_y"].apply(mass_to_ele)
print(inner_df[:2])

file_path = 'ffnonbonded.csv'
try:
    df = pd.read_csv(file_path,index_col=0)
except:
    df = pd.DataFrame()
df_concatenated = pd.concat([df,inner_df], ignore_index=True)
df_unique = df_concatenated.drop_duplicates(subset=['atomstype'])
df_unique.to_csv(file_path)

with open('pdb2data/ffnonbonded.itp', 'w') as f:
    f.write('[ atomtypes ]\n')
    for index, row in df_unique.iterrows():
        f.write('{} {} {} {} {} {} {} {} \n'.format(row['atomstype'],row['atom_name_y'],row['atom_ele']   ,row['atom_mass'] ,row['charge'],row['xxx'],row['par1']    ,row['par2']           ))

###########################

file_path = 'ffbonded.csv'
try:
    df = pd.read_csv(file_path,index_col=0)
except:
    df = pd.DataFrame()
df_concatenated = pd.concat([df,itp_bonds_df], ignore_index=True)
df_unique = df_concatenated.drop_duplicates(subset=['atom1', 'atom2'])
df_unique.to_csv(file_path)

with open('pdb2data/ffbonded.itp', 'w') as f:
    f.write('[ bondtypes  ]\n')
    for index, row in df_unique.iterrows():
        f.write('{} {} {} {} {}\n'.format(row['atom1'],   row['atom2'],row['xxxx'],row['num1'],row['num2'] ))


#################################
