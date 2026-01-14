#!/bin/bash

echo "SCF calcultation" && cd 01_scf
#python scf_from_vcrelax.py
mpirun -np 16 pw.x < ZnO.scf.in > ZnO.scf.out 2>&1
cd ..

echo "NSCF calculation" && cd 02_nscf
mpirun -np 16 pw.x < ZnO.nscf.in > ZnO.nscf.out 2>&1
cd ..

echo "Post processing with dos.x and projwfc.x" && cd 03_ppdos
dos.x < dos.in > dos.out 2>&1
projwfc.x < projwfc.in > projwfc.out 2>&1
echo "CALCULATION DONE!"

