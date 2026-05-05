#!/bin/bash
JOBID="Contour Plot E(a,c) : BN-ZnO"

PWI_DIR="pwi_new"
cd $PWI_DIR

echo "Starting SCF calculations for Eac scan... $(date +%F) $(date +%T)"

for f in $(ls); do

    f_out="${f%.*}.out"
    echo
    echo "=============================================="
    echo "Running $f at $(date +%T)"
    mpirun -np 16 pw.x <  $f > $f_out
    echo "Finished:  $f_out at $(date +%T)"
    echo "=============================================="
    echo

done

SCRIPT_DIR="/home/jvc/ZnO_database/scripts"
cd "$SCRIPT_DIR"
python send_email.py "$JOBID finalizado! "
