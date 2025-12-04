#!/bin/bash

export OMP_NUM_THREADS=1


# Criação dos inputs.
echo "Processo iniciado. $(date +%F' '%T)"

for ecutwfc in {20..150..10}; do
# Norm-Conserving Pseudo Dojo
ecutrho=$((4 * $ecutwfc)) 

sed -e 's/ECUTWFC/'"$ecutwfc"'/g' \
    -e 's/ECUTRHO/'"$ecutrho"'/g' ZnO_LDA_template.in > scf_wfc${ecutwfc}_rho${ecutrho}.in
done
echo "Criando diretório para os inputs"
mkdir -p "scf_inputs"

echo "Criando diretório para os outputs"
mkdir -p "scf_outputs"

echo "Movendo arquivos de input para o diretório scf_inputs"
mv scf_*.in scf_inputs/

echo "Dentro do diretório scf_inputs"
cd scf_inputs

echo "Iniciando os cálculos de SCF"
# Rodandos os inputs scf's
for file in $(ls scf*.in); do
    echo "Running SCF for input file: $file"
    mpirun -np 16 pw.x < "$file" > "../scf_outputs/${file%.in}.out" 2>&1
done
echo "SCF Finalizados."
cd ..



echo "Processo concluído. $(date +%F' '%T)"