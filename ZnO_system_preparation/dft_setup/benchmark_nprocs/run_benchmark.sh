#!/bin/bash

# Caminho para o executável pw.x do Quantum ESPRESSO
PW_EXEC="../../bin/pw.x"              # ou "/caminho/para/pw.x" se não estiver no PATH
INPUT_FILE="ZnO.in"         # Nome do arquivo de entrada
LOG_DIR="benchmark_logs"    # Diretório para armazenar os logs
OUTPUT_FILE="ZnO.out"       # Arquivo de saída padrão
NPROC_LIST=(12)  # Lista de números de processadores a testar

mkdir -p "$LOG_DIR"

for NPROC in "${NPROC_LIST[@]}"; do

    START=$(date +%s.%N)

    mpirun -np "$NPROC" "$PW_EXEC" -in "$INPUT_FILE" > "${LOG_DIR}/output_${NPROC}proc.log"

    END=$(date +%s.%N)
    ELAPSED=$(echo "$END - $START" | bc)

    echo "Tempo com ${NPROC} processo(s): ${ELAPSED} segundos" | tee -a "${LOG_DIR}/timing_summary.txt"
done

echo -e "\nBenchmark finalizado. Verifique os logs em $LOG_DIR/"
