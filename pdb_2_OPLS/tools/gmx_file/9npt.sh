

cd min 
cd cg

cd tuihuo

cd npt 


cd npt_2
mkdir npt_3
cd npt_3

cp ../gromacs_run.top ./
cp ../*.itp ./

old=npt2
new=npt3

echo '
integrator = md
dt = 0.001 ; ps
nsteps = 2000000

nstxout-compressed = 1000
;compressed-x-grps  = system
nstxout = 5000
nstvout = 5000
nstfout = 5000
;nstlog  = 5000
nstenergy = 5000

; Nonbonded settings 
cutoff-scheme           = Verlet    ; Buffered neighbor searching
ns_type                 = grid      ; search neighboring grid cells
;nstlist                 = 10        ; 20 fs, largely irrelevant with Verlet
rcoulomb                = 1.0       ; short-range electrostatic cutoff (in nm)
rvdw                    = 1.0       ; short-range van der Waals cutoff (in nm)
DispCorr                = EnerPres  ; account for cut-off vdW scheme


; Electrostatics
;coulombtype             = PME       ; Particle Mesh Ewald for long-range electrostatics
;pme_order               = 4         ; cubic interpolation
;fourierspacing          = 0.16      ; grid spacing for FFT

;rlist = 2
coulombtype = cut-off
;rcoulomb = 2
vdwtype = cut-off
;rvdw = 2




; Bond parameters
continuation            = yes       ; Restarting after NVT 
constraint_algorithm    = lincs     ; holonomic constraints 
constraints             = h-bonds   ; bonds involving H are constrained
lincs_iter              = 1         ; accuracy of LINCS
lincs_order             = 4         ; also related to accuracy





Pcoupl     = Berendsen
pcoupltype = isotropic
tau_p = 1
ref_p = 1
compressibility = 4.5e-5


;Pcoupl     = Parrinello-Rahman
;pcoupltype = isotropic
;tau_p = 2.5
;ref_p = 1
;compressibility = 4.5e-5


Tcoupl = v-rescale
tau_t = 0.2
ref_t = 300
tc_grps = system


'  > $new.mdp




gmx grompp -f $new.mdp -c ../$old.gro -p gromacs_run.top  -o $new.tpr -maxwarn 3
gmx mdrun -v -deffnm $new -nt 4

gmx trjconv -s $new.tpr -f $new.xtc -o prod_whole.xtc -pbc whole

#gmx trjconv -f min.trr -o min.xtc -dt 1 -pbc mol -s min.tpr

