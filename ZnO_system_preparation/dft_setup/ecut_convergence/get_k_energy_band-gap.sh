#!/bin/bash

# Limpa o arquivo de saída para evitar duplicatas caso o script seja rodado mais de uma vez
> dados_ecut.dat

# Itera sobre valores de k
for ecut in 30 50 70 90 110 130 150; do
    arquivo_saida="ecut_${ecut}.out"
    
    # Extrai energia total
    energia_total=$(awk '/^!/{print $5; exit}' "$arquivo_saida")
    
    # Extrai band gap forçando ponto decimal
    band_gap=$(LC_NUMERIC=C awk '/highest occupied, lowest unoccupied level \(ev\):/ {gap = $8 - $7; printf "%.4f", gap}' "$arquivo_saida")
    
    # Escreve k, energia total e band gap em uma linha
    echo "$k $energia_total $band_gap" >> dados_ecut.dat
done
