#!/bin/bash
# ============================================================
# Script: run_disp_scf.sh
# Executa todos os arquivos disp*.pw.in
# ============================================================


PWX="${HOME}/pw_intel.x"

# Número de processadores
NP=64

# Loop sobre todos os arquivos disp*.pw.in
for infile in disp*.pw.in; do
    outfile="${infile%.in}.out"
    echo "==> Rodando $infile ..."
    mpirun -np $NP $PWX -nk 4 -nd 16 -in "$infile" > "$outfile"
done

echo "Finalizado."
