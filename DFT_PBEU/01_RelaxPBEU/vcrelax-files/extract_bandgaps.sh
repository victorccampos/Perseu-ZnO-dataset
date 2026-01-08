#!/bin/bash
# ==============================================================================
# Descrição: Extrai o gap de energia (Highest Occupied - Lowest Unoccupied)
#            de arquivos de saída do Quantum ESPRESSO (.out).
#
# IMPORTANTE (Lógica do vc-relax):
# Este script foi desenhado para cálculos de relaxamento (vc-relax ou relax).
# O Quantum ESPRESSO imprime a linha "highest occupied" múltiplas vezes
# durante a otimização da geometria.
#
# O comando 'awk' abaixo lê o arquivo inteiro, mas as variáveis só retêm
# os valores da ÚLTIMA ocorrência encontrada. Portanto, o gap calculado
# corresponde exclusivamente à ESTRUTURA FINAL RELAXADA.
# ==============================================================================


OUTPUT_DATA="bandgaps.dat"

echo "highest_occupied lowest_unoccupied Egap" > $OUTPUT_DATA

for file in $(ls ZnO*.out); do
    echo "Processing $file"
    awk '/highest occupied/ {ho=$7; lu=$8} END {print FILENAME, ho, lu, lu-ho}' "$file" >> "$OUTPUT_DATA"
done
cd ..

cp $OUTPUT_DATA ..
echo "Bandgap extraction complete. Results saved in bandgaps.dat"
