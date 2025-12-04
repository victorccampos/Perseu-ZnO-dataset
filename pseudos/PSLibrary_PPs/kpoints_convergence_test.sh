#!/bin/bash
# Convergence test of k-points grid.Set a variable k-point from 4 to 15.

for k in 3 4 5 6 7 8 9 10 11 12 13 14 15; do

# Make input file for the SCF calculation.
cat > scf_kpoint.$k.in << EOF
&CONTROL
  calculation = 'scf'
  prefix = 'ZnO_GGA_U'
  pseudo_dir = '/home/jvc/QEspresso7.2/ZnO_database/pseudos/PSLibrary_PPs'
  outdir='.'
  disk_io = 'none'
  verbosity = 'high'
  tstress=.true.
  tprnfor=.true.
/
&SYSTEM
    ibrav= 4
    celldm(1) = 6.19
    celldm(3) = 1.60
    ntyp= 2
    nat=  4
    ecutwfc =  90
    ecutrho = 720 ! 90 x 8
    occupations = 'fixed'
    nbnd =  36
/
&ELECTRONS
    conv_thr = 1.0d-9
    mixing_beta = 0.3
    electron_maxstep = 120
/
/
ATOMIC_SPECIES
Zn   65.380    Zn.upf
 O   15.999    O.upf

K_POINTS automatic
$k $k $((k-2))  0  0  0

ATOMIC_POSITIONS (crystal)
Zn   0.3333333333   0.6666666667   0.0000000000
Zn   0.6666666667   0.3333333333   0.5000000000
O    0.3333333333   0.6666666667   0.3800000000  ! u parameter aprox 0.38
O    0.6666666667   0.3333333333   0.8800000000

EOF


# Run pw.x for SCF calculation.
mpirun -np 16 "pw.x" < scf_kpoint.$k.in > scf_kpoint.$k.out
done
