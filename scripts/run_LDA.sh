#!/bin/bash

# 1. Lista os arquivos .in
# 2. Usa o '-' como delimitador para ordenar pela 4ª coluna (-k4,4) numericamente (-n)
# 3. Itera sobre essa lista ordenada

echo "Início de Criação do Dataset [$(date +%F)] $(date +%T)"

input_dir="LDA_000_INPUTS"
cd $input_dir

files=$(ls ZnO-*.in | sort -t '-' -k4,4n)


for file in $files; do
    output="${file%.in}.out"
    echo
    echo "------------- RUN [$(date +%F)] $(date +%T) -------------"
    echo "[IN/OUT]: $file --> $output "
    #mpirun -np 32 pw.x -nk 2 < "$file" > "../LDA_000_OUTPUTS/$output"
    
    echo "FINALIZADO: [$(date +%F)] $(date +%T)"
    echo "---------------------------------------------------------"
    echo
done