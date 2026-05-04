#!/bin/bash

JOBID="New LDA Dataset - $(date)"
python send_email.py "$JOBID submitted!"


INPUT_DIR="LDA_dataset2_pwis"
OUTPUT_DIR="LDA_dataset2_pwos"

mkdir -p "$OUTPUT_DIR"

echo "Início do RESTART [$(date +%F)] $(date +%T)"

files=$(ls "$INPUT_DIR"/ZnO-*.in | sort -t '-' -k4,4n)

for filepath in $files; do
    file=$(basename "$filepath")
    output="${file%.in}.out"
    outpath="$OUTPUT_DIR/$output"

    # Skip if already completed 
    if [ -f "$outpath" ] && grep -q "JOB DONE" "$outpath"; then
        echo "SKIPPING (already done!): $file"
        continue
    fi

    echo "------------- RUN [$(date +%F)] $(date +%T) -------------"
    echo "[IN/OUT]: $file --> $output"

    mpirun -np 32 pw.x < "$INPUT_DIR/$file" > "$outpath"

    echo "FINALIZADO: [$(date +%F)] $(date +%T)"
    echo "---------------------------------------------------------"
    echo
done

python send_email.py "$JOBID finished!"
