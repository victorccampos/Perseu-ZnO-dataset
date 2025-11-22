#!/bin/bash
# Convergence test of k-points grid.Set a variable k-point from 4 to 12.

for k in $(seq 4 1 12); do
# Make input file for the SCF calculation.
cat > scf_kpoint.$k.in << EOF
!Optimal Lattice Parameters (Bohr):
!	Lattice Parameter a = 6.1003
!	Lattice Parameter c = 9.8520
!	Ratio c/a = 1.6150
&CONTROL
  calculation = 'scf',
  pseudo_dir = '../pseudos_PBE_Opium',
  outdir='.'
  prefix = 'ZnO_opium_${k}',
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
    ecutwfc =  70,
    ecutrho = 350,
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
 $k $k ${k-2}  0  0  0

ATOMIC_POSITIONS (crystal)
Zn               0.6666666667        0.3333333333        0.5006738064
Zn               0.3333333333        0.6666666667        0.0006738064
O                0.6666666667        0.3333333333        0.8796361936
O                0.3333333333        0.6666666667        0.3796361936
EOF

# Run pw.x for SCF calculation.
mpirun -np 16 "$HOME/pw_intel.x" < scf_kpoint.$k.in > scf_kpoint.$k.out

# Write the number of k-points (= k*k*1) and the total energy in calc-kpoint.dat
awk -v k=$k '/!/ {printf "%dx%dx%d %s\n", k, k, k-2, $5}' scf_kpoint.$k.out >> kpoints_convergence_energies.dat
# End of for loop.
done
