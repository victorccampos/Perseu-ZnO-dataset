#!/bin/bash
# USPP PSLibrary convergence test on ecutwfc and ecutrho for ZnO

MULT_ECUTRHO=8

for ecutwfc in {20..150..10}; 
do
    ecutrho=$((MULT_ECUTRHO * ecutwfc))
    
    mkdir -p inputs outputs # Directories for input and output files
    
    cat > inputs/scf_ecutwfc.${ecutwfc}.${mult_ecutrho}.in << EOF
&CONTROL
  calculation = 'scf',
  pseudo_dir = '../pseudos',
  outdir='.'
  prefix = 'ZnO_PSL_${ecutwfc}',
  verbosity = 'high',
  tstress=.true.,
  tprnfor=.true.,
  disk_io = 'none'
/
&SYSTEM
    ibrav= 4,
    celldm(1) = 6.1003,
    celldm(3) = 1.6150,
    ntyp= 2
    nat=  4,
    ecutwfc =  $ecutwfc,
    ecutrho = $ecutrho,
    occupations = 'fixed',
    nbnd =  36,
    degauss = 0.005,
    smearing = 'gaussian',
/
&ELECTRONS
    diagonalization = 'david'
    mixing_mode='local-TF',
    conv_thr= 1.0d-9,
    mixing_beta=0.1,
    electron_maxstep=190,
/

ATOMIC_SPECIES
Zn   65.380    Zn.upf
 O   15.999    O.upf

K_POINTS automatic
 6 6 4  0  0  0

ATOMIC_POSITIONS (crystal)
Zn               0.6666666667        0.3333333333        0.5006738064
Zn               0.3333333333        0.6666666667        0.0006738064
O                0.6666666667        0.3333333333        0.8796361936
O                0.3333333333        0.6666666667        0.3796361936
EOF
    mpirun -np 8 "$HOME/pw_intel.x" < inputs/scf_ecutwfc.${ecutwfc}.${MULT_ECUTRHO}.in > outputs/scf_ecutwfc.${ecutwfc}.${MULT_ECUTRHO}.out

done


