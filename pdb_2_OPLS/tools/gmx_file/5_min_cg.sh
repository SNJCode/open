

cd min 

mkdir cg
cd cg
cp ../gromacs_run.top ./
cp ../*.itp ./

echo ';define = -DFLEXIBLE
integrator = cg
nsteps =-1
emtol  = 500.0
emstep = 0.01
;
nstxout   = 100
nstlog    = 50
nstenergy = 50
;
pbc = xyz
cutoff-scheme            = Verlet
coulombtype              = PME
rcoulomb                 = 1.0
rvdw                     = 1.0
DispCorr                 = EnerPres
;
constraints              = none
'  > cg.mdp


gmx grompp -f cg.mdp -c ../min.gro -p gromacs_run.top  -o cg.tpr -maxwarn 1
gmx mdrun -v -deffnm cg -nt 4

#gmx trjconv -f min.trr -o min.xtc -dt 1 -pbc mol -s min.tpr

