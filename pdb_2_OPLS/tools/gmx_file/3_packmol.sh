
ff=$1
cat topol.top | sed -n  '/\[ moleculetype \]/,/; Include Position restraint file/p' | sed 's/Protein/'$ff'/g' > $ff.itp


mm=$(cat $ff.itp | awk '{print NR,$0}'| sed -n '/\[ dihedrals \]/,//p' | awk '{ if(NF==6) print $0 }' | awk '{print $1}' )
nn=$(echo $mm | sed 's/ /d;/g')
sed -i ''${nn}'d' $ff.itp 


mm=$(cat $ff.itp | awk '{print NR,$0}'| sed -n '/\[ angles \]/,//p' | awk '{ if(NF==5) print $0 }' | awk '{print $1}' )
nn=$(echo $mm | sed 's/ /d;/g')
sed -i ''${nn}'d' $ff.itp 



echo '# Packmol 输入文件示例

# 定义模拟盒子
tolerance 2.0
add_box_sides 1.2
output packout.pdb

# 定义分子 1: 水分子
structure output.pdb
  number '$2'
  inside box 0.0 0.0 0.0 150 150 150
end structure

'  > xx

packmol < xx


echo '

; Include forcefield parameters
#include "oplsaa.ff/forcefield.itp"


#include "'$ff'.itp"


[ system ]
; Name
TEEST

[ molecules ]
; Compound        #mols
'$ff'        	'$2'
' > gromacs_run.top
