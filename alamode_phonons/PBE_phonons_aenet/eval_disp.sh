#!/bin/bash

for f in lmp_harm*.lammps; do
    base="${f%.lammps}"
    echo "Running for $f ..."
    echo "Base name: $base"
    cp "$f" tmp.lammps
    mpirun -np 1 $HOME/MLFF/lammps-4Feb20/src/lmp_mpi < md.lmp > "log.${base}"
    cp XFSET "XFSET.${base}"
done
