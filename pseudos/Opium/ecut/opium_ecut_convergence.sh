#!/bin/bash
# Convergence test of ecutwfc and ecutrho on larger k-grid

mkdir -p inputs
mkdir -p outputs
cd inputs || exit 1
for ecutwfc in {20..150..10}; do
ecutrho=$((4 * ecutwfc))
# Make input file for the SCF calculation.
cat > scf_ecutwfc.$ecutwfc.in << EOF
!Optimal Lattice Parameters (Bohr) from vc-relax calculation:
!	Lattice Parameter a = 6.1003
!	Lattice Parameter c = 9.8520
!	Ratio c/a = 1.6150
&CONTROL
  calculation = 'scf',
  pseudo_dir = '/home/jvc/QEspresso7.2/ZnO_database/ZnO_PBE_Opium/pseudos_PBE_Opium',
  outdir='.'
  prefix = 'ZnO_opium_${ecutwfc}',
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
Zn   63.380    Zn.upf
 O   15.999    O.upf

K_POINTS automatic
 6 6 4  0  0  0

ATOMIC_POSITIONS (crystal)
Zn               0.6666666667        0.3333333333        0.5006738064
Zn               0.3333333333        0.6666666667        0.0006738064
O                0.6666666667        0.3333333333        0.8796361936
O                0.3333333333        0.6666666667        0.3796361936
EOF


# Run pw.x for SCF calculation.
mpirun -np 16 "$HOME/pw_intel.x" < scf_ecutwfc.$ecutwfc.in > ../outputs/scf_ecutwfc.$ecutwfc.out

echo "Completed ecutwfc = $ecutwfc, ecutrho = $ecutrho"
done

echo "Done all calculations."

