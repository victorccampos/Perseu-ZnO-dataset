#!/bin/bash

#### Convergence test of k-points grid.

# Set a variable k-point from 4 to 14
for k in 6 8 10 12 14 16 20 30 40; do

# Make input file for scf calculation with relaxed structure
# k-points grid is assigned by variable n
cat > kpoint.$k.in << EOF
&CONTROL
  calculation = 'scf',
  restart_mode = 'from_scratch',
  !restart_mode = 'restart',
  pseudo_dir = '../pseudos',
  outdir='.'
  prefix = 'ZnO_PBE_bulk',
  nstep=450,
  verbosity = 'high',
  tstress=.true.,
  tprnfor=.true.,
  forc_conv_thr=1.0d-5,
  etot_conv_thr=1.0d-6,
/
&SYSTEM
    ibrav= 4,
    celldm(1) = 6.194571412,
    celldm(3) = 1.614358356,
    ntyp= 2,
    nat=  4,
    ecutwfc =  70,
    ecutrho = 350,
    occupations = 'fixed',
    nbnd =  72,
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
Zn   63.380    Zn.upf
 O   15.999    O.upf


K_POINTS automatic
 ${k} ${k} ${k}  0  0  0


ATOMIC_POSITIONS (crystal)
Zn            0.6666666667        0.3333333333        0.5006426381
Zn            0.3333333333        0.6666666667        0.0006426381
O             0.6666666667        0.3333333333        0.8796673619
O             0.3333333333        0.6666666667        0.3796673619
EOF

# Run pw.x for SCF calcultation
conda deactivate; nohup mpirun -np 60 ../../bin/pw.x < kpoint.$k.in > kpoint.$k.out

# Write the number of k-point and the total energy in calc-kpoint.dat
awk '{printf"%d %s\n", '$k, $5'}' kpoint.$k.out >> calc-kpoint.dat

# End of for loop
done

