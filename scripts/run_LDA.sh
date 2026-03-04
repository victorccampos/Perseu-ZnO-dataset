#!/bin/bash

# 1. Lista os arquivos .in
# 2. Usa o '-' como delimitador para ordenar pela 4ª coluna (-k4,4) numericamente (-n)
# 3. Itera sobre essa lista ordenada
JOBNAME="LDA_006"
echo "Início de Criação do Dataset [$(date +%F)] $(date +%T)"

input_dir="LDA_004_INPUTS"
cd $input_dir

files=$(ls ZnO-*.in | sort -t '-' -k4,4n)


for file in $files; do
    output="${file%.in}.out"
    echo
    echo "------------- RUN [$(date +%F)] $(date +%T) -------------"
    echo "[IN/OUT]: $file --> $output "
    mpirun -np 32 pw.x -nk 2 < "$file" > "../LDA_004_OUTPUTS/$output"
    
    echo "FINALIZADO: [$(date +%F)] $(date +%T)"
    echo "---------------------------------------------------------"
    echo
done

# Manda um e-mail avisando que o processo terminou
python send_email.py "$JOBNAME finished!"
