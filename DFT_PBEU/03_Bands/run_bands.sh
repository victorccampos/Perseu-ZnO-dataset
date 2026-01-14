#!/bin/bash

scf_input="ZnO-scf.in"
nscf_input="ZnO-nscf.in"
pp_bands_input="ZnO-ppbands.in"

echo "Running Band Structure Calculation for ZnO using Quantum ESPRESSO"
echo "$(date +%Y-%m-%d\ %H:%M:%S)"

cd "scf/"
echo "Running Self-Consistent Calculation"
mpirun -np 16 pw.x < "$scf_input" > ${scf_input%.in}.out
cd ..

cd "nscf/"
echo "Running Non Self-Consistent Calculation"
mpirun -np 16 pw.x < "$nscf_input" > ${nscf_input%.in}.out
cd ..

cd "pp-bands/"
echo "Post-Processing Bands"
bands.x < "$pp_bands_input" > ${pp_bands_input%.in}.out
cd ..

echo "Job Done"
echo "$(date +%Y-%m-%d\ %H:%M:%S)"
echo "=============================="