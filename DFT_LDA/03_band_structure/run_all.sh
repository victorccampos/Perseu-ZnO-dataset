#!/bin/bash

SCF_FOLDER="scf"
NSCF_FOLDER="nscf"
PP_BANDS_FOLDER="pp_bands"

#LOG_FILE="run_all.log"

echo "Starting band structure calculations: [$(date)]"
#exec > >(tee -a "$LOG_FILE") 2>&1 # Log stdout and stderr to file
# ============================================================================ #
cd $SCF_FOLDER
input="01_ZnO_scf.in"
echo "Running SCF calculation with input file: $input"
mpirun -np 16 pw.x -inp $input > ${input%.in}.out
cd ..
# ============================================================================ #
cd $NSCF_FOLDER
input="02_ZnO_nscf.in"
echo "Running NSCF calculation: "
mpirun -np 16 pw.x -inp $input > ${input%.in}.out
cd ..
# ============================================================================ #
cd $PP_BANDS_FOLDER
input="03_ZnO_bands.in"
echo "Running post-processing with bands.x:"
mpirun bands.x -inp $input > ${input%.in}.out
cd ..
# ============================================================================ #
echo "JOB DONE: [$(date)]"
