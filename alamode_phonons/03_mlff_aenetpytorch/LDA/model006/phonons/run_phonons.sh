#!/bin/bash

# Interrupt if any command fails
set -e

LAMMPS_BIN="$HOME/AENET-LAMMPS/lammps-4Feb20/src/lmp_mpi"
EXTRACT_PY="$HOME/alamode/tools/extract.py"

# Set common files for models
COMMON="/home/victorcampos/aenet-PyTorch/DatasetLDA/common"
INPUT_LMP="$COMMON/in.lmp"
reference_structure="$COMMON/ZnO_lda_supercell.lammps"
displaced_structures="$COMMON/displaced/"
optimize_input="$COMMON/optimize.in"
anphon_input="$COMMON/anphon_NA0.in"

# Check if reference structure exists and its a file
if [[ ! -f "$reference_structure" ]]; then
    echo "Error: Reference structure '$reference_structure' not found."
    exit 1
fi

# Check if displaced structures directory exists and is a directory
if [[ ! -d "$displaced_structures" ]]; then
    echo "Error: Displaced structures directory '$displaced_structures' not found."
    exit 1
fi


function clean_run() {
    rm -rf anphon_NA0.{in,out} optimize.{in,out} tmp.lammps log.lammps *XFSET* xfset *.bands *.fcs *.xml *.nn
}

function run_reference_structure() {
    # Run reference structure of common folder and save results in current model folder
    cp "$reference_structure" tmp.lammps
    "$LAMMPS_BIN" < "$INPUT_LMP" > log.lammps
    mv XFSET XFSET.reference
   
    
}


function run_displaced_structures() {
    mkdir -p xfset
    for f in "$displaced_structures"/*.lammps; do
        base=$(basename "$f" .lammps)

        rm -f XFSET tmp.lammps log.lammps
        cp "$f" tmp.lammps

        "$LAMMPS_BIN" < "$INPUT_LMP" > "xfset/${base}.log"
        mv XFSET "xfset/XFSET.${base}"
    done
}

function extract_harmonic() {
    
    conda run --name alamode python $EXTRACT_PY --LAMMPS=$reference_structure --offset=XFSET.reference xfset/XFSET.zno_mlff* > XFSET_harmonic
}


function run_optimize() {
    cp $optimize_input .
    local filein=$(basename $optimize_input) 
    conda run --name alamode alm $filein > "${filein%.in}.out" 
}

function run_anphon() {
    cp $anphon_input .
    local filein=$(basename $anphon_input) 
    conda run --name alamode anphon $filein > "${filein%.in}.out"

    # Create a copy of .bands file with id of the model, e.g, the pwd name
    # local model_id=$(basename "$PWD")
    # local bands_file=$(ls *.bands 2>/dev/null)
    # cp  bands_file "${model_id}.bands"
}

function run_workflow(){

run_reference_structure
run_displaced_structures
extract_harmonic
run_optimize
run_anphon

}


echo "Cleaning previous run"
clean_run
sleep 5

echo "Copying networks to current directory"
cp ../*.pytorch.nn $PWD
echo "Running Workflow"
sleep 3

run_workflow



