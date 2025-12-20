#!/bin/bash

# Calculation of Density of States and Partial Density of States.
mpirun -np 16 pw.x < scf.ZnO_hubbard.in > scf.ZnO_hubbard.out 2>&1
mpirun -np 16 pw.x < nscf.ZnO_hubbard.in > nscf.ZnO_hubbard.out 2>&1
mpirun -np 16 dos.x < dos.ZnO_hubbard.in > dos.ZnO_hubbard.out 2>&1
mpirun -np 16 projwfc.x < projwfc.ZnO_hubbard.in > projwfc.ZnO_hubbard.out 2>&1
