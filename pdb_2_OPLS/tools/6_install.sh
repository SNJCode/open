path=$(which gmx)

path=${path%/*}
path=${path%/*}
top=$path/share/gromacs/top

#mkdir save_gromcas

pp=$(pwd)

mol=$1
mol=$(echo $mol | sed 's/\///g')

cd $mol/creat_itp/pdb2data
echo $top

#cp ${top}/residuetypes.dat  ${pp}/save_gromcas


echo ';DELETE START' >> ${top}/residuetypes.dat
cat residuetypes.dat >> ${top}/residuetypes.dat
echo ';DELETE END' >> ${top}/residuetypes.dat

########################################

opls=$path/share/gromacs/top/oplsaa.ff
#cp ${opls}/atomtypes.atp ${pp}/save_gromcas


echo ';DELETE START' >>  ${opls}/atomtypes.atp
cat atomtypes.atp >> ${opls}/atomtypes.atp
#echo ';DELETE END' >> ${opls}/atomtypes.atp


########################################
#cp ${opls}/ffbonded.itp  ${pp}/save_gromcas


echo ';DELETE START' >> ${opls}/ffbonded.itp
cat ffbonded.itp   >> ${opls}/ffbonded.itp
echo ';DELETE END' >>${opls}/ffbonded.itp

########################################

#cp ${opls}/ffnonbonded.itp  ${pp}/save_gromcas

echo ';DELETE START' >> ${opls}/ffnonbonded.itp
cat ffnonbonded.itp | sed '1d'  >> ${opls}/ffnonbonded.itp
echo ';DELETE END' >> ${opls}/ffnonbonded.itp


cp *.rtp ${opls}
