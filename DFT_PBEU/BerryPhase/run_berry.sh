#!/bin/bash

scf_input="ZnO-BP-scf.in"
nscf_input="ZnO-BP-nscf.in"

echo "Starting Berry Phase Calculation"

mpirun -np 16 pw.x -in $scf_input > ${scf_input%.in}.out
mpirun -np 16 pw.x -in $nscf_input > ${nscf_input%.in}.out

echo "Finished Berry Phase Calculation"
