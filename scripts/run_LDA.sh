#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
JOBNAME="LDA_012"

# Diretórios de trabalho
INPUT_DIR="$SCRIPT_DIR/${JOBNAME}_INPUTS"
OUTPUT_DIR="$SCRIPT_DIR/${JOBNAME}_OUTPUTS"
EMAIL_SCRIPT="$SCRIPT_DIR/send_email.py"

echo "Início de Criação do Dataset [$(date +%F)] $(date +%T)"
python "$EMAIL_SCRIPT" "$JOBNAME Submitted!"

cd "$INPUT_DIR" || {
    echo "Erro: não foi possível entrar em $INPUT_DIR"
    python "$EMAIL_SCRIPT" "$JOBNAME failed: could not enter input dir"
    exit 1
}

files=$(ls ZnO-*.in 2>/dev/null | sort -t '-' -k4,4n)

if [ -z "$files" ]; then
    echo "Erro: nenhum arquivo ZnO-*.in encontrado em $INPUT_DIR"
    python "$EMAIL_SCRIPT" "$JOBNAME failed: no input files"
    exit 1
fi

for file in $files; do
    output="${file%.in}.out"
    echo
    echo "------------- RUN [$(date +%F)] $(date +%T) -------------"
    echo "[IN/OUT]: $file --> $output"
    mpirun -np 32 pw.x -nk 2 < "$file" > "$OUTPUT_DIR/$output"
    echo "FINALIZADO: [$(date +%F)] $(date +%T)"
    echo "---------------------------------------------------------"
    echo
done

cd "$SCRIPT_DIR" || exit 1

python "$EMAIL_SCRIPT" "$JOBNAME finished!"
