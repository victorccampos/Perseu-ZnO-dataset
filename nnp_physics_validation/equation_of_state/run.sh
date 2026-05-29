#!/bin/bash


LAMMPS_BIN="$HOME/MLFF_AENET-v2.4/lammps-4Feb20/src/lmp_mpi"
INPUT_LMP="in.lmp"
temp_file="temp.lammps"
for data_file in $(ls lammps_v*.data); do
    echo "Running LAMMPS for $data_file"

    cp $data_file $temp_file
    lmp_mpi -in $INPUT_LMP > log_${data_file%.data}.txt

done
