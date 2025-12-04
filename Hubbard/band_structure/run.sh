#!/bin/bash

mpirun -np 16 pw.x < scf.ZnO_hubbard.in > scf.ZnO_hubbard.out 2>&1
mpirun -np 16 pw.x < nscf.ZnO_hubbard.in > nscf.ZnO_hubbard.out 2>&1
mpirun -np 4 bands.x < bands.in > bands.out 2>&1
mpirun -np 4 bands.x < dos.in > dos.out 2>&
