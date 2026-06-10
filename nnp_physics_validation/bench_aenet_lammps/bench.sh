#!/bin/bash


for NP in 40 48 56 60 64; do
    echo "Running 2000 steps with np = $NP:"
    mpirun -np "$NP" lmp_mpi -log "${NP}procs.log" -in in.benchmark  > "${NP}.procs.out"
done

echo "Benchmark concluído"
