path=$(which gmx)

path=${path%/*}
path=${path%/*}
top=$path/share/gromacs/top

pp=$(pwd)


delnum () {


sta=$(cat $1 | grep -n ';DELETE START'  | sed -n '1p' | awk -F : '{print $1}')

end=$(cat $1 | grep -n ';DELETE END'  | sed -n '$p' | awk -F : '{print $1}')

if [ ! -z  $sta ] ;then
	echo unintall $1
	sed -i "${sta},${end}d" $1
fi
}

opls=$path/share/gromacs/top/oplsaa.ff

delnum  ${top}/residuetypes.dat
delnum  ${opls}/ffbonded.itp
delnum  ${opls}/ffnonbonded.itp


atp=${opls}/atomtypes.atp
sta=$(cat $atp  | grep -n ';DELETE START'  | sed -n '1p' | awk -F : '{print $1}')
if [ ! -z  $sta ] ;then
	echo unintall $atp
	sed -i ''${sta}',$d' $atp
fi

