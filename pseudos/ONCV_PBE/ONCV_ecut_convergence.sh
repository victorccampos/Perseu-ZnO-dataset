#!/bin/bash

export OMP_NUM_THREADS=1
echo "Processo iniciado em $(pwd) == $(date +%F' '%T)"

for ecutwfc in {20..150..10}; do
# Norm-Conserving Pseudo Dojo
ecutrho=$((4 * $ecutwfc))

sed -e 's/ECUTWFC/'"$ecutwfc"'/g' \
    -e 's/ECUTRHO/'"$ecutrho"'/g' ZnO_LDA_template.in > scf_wfc${ecutwfc}_rho${ecutrho}.in
done

echo "Criando diretório para os inputs e outputs"
mkdir -p "scf_inputs"
mkdir -p "scf_outputs"

mv scf_*.in scf_inputs/
cd scf_inputs

echo "Iniciando os cálculos de SCF"
for file in $(ls scf*.in); do
    echo "Running SCF for input file: $file"
    mpirun -np 16 "$HOME/pw_intel.x" < "$file" > "../scf_outputs/${file%.in}.out" 2>&1
done
echo "SCF Finalizados."

cd ..


echo "Processo concluído. $(date +%F' '%T)"
