
mkdir min
cd min 
cp ../packout.pdb ./
cp ../gromacs_run.top ./
cp ../*.itp ./
gmx  editconf -f packout.pdb -o new.gro -d 1.0 -c -bt cubic
echo '; minim.mdp - used as input into grompp to generate em.tpr
integrator  = steep     ; Algorithm (steep = steepest descent minimization)
emtol       = 1000    ; Stop minimization when the maximum force < 1000.0 kJ/mol/nm
emstep      = 0.01      ; Energy step size
nsteps      = -1     ; Maximum number of (minimization) steps to perform

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
nstlist         = 10         ; Frequency to update the neighbor list and long range forces
cutoff-scheme   = Verlet
ns_type         = grid      ; Method to determine neighbor list (simple, grid)
coulombtype     = PME       ; Treatment of long range electrostatic interactions
rcoulomb        = 1.0       ; Short-range electrostatic cut-off
rvdw            = 1.0       ; Short-range Van der Waals cut-off
pbc             = xyz       ; Periodic Boundary Conditions (yes/no)
'  > minim.mdp


gmx grompp -f minim.mdp -c new.gro -p gromacs_run.top -o min.tpr -maxwarn 2
gmx mdrun -v -deffnm min -nt 4

#gmx trjconv -f min.trr -o min.xtc -dt 1 -pbc mol -s min.tpr

