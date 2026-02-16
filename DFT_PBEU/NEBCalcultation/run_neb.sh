#!/bin/bash
mkdir -p "neb_outputs"

echo "================================"
echo "Starting NEB calculation with 12 processors"

mpirun -np 12 neb.x -ni 3 -i neb.in > neb.out

echo "NEB calculation completed $(date)"
echo "================================"


echo "================================"
echo "Moving output files to neb_outputs directory"

mv ZnO_PBEU_NEB.* neb_outputs
mv pw_* out.* neb_outputs

echo "================================"
