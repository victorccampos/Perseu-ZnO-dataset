### Possíveis causas:
1. **Separador decimal:** O uso da vírgula (`,`) em vez do ponto (`.`) sugere que o locale do seu sistema pode estar usando vírgula como separador decimal. O awk normalmente usa ponto.
2. **Posição dos campos:** Talvez os campos `$6` e `$7` não estejam corretos para o seu arquivo. Vamos conferir isso.

### Como diagnosticar

Rode este comando para ver exatamente como awk está enxergando os campos:

```bash
awk '/highest occupied, lowest unoccupied level \(ev\):/ {for(i=1;i dados.dat

for k in 6 8 10 12 14 16 20 30; do
    arquivo_saida="kpoint.${k}.out"
    
    energia_total=$(awk '/^!/{print $5; exit}' "$arquivo_saida")
    band_gap=$(LC_NUMERIC=C awk '/highest occupied, lowest unoccupied level \(ev\):/ {gap = $8 - $7; printf "%.4f", gap}' "$arquivo_saida")
    
    echo "$k $energia_total $band_gap" >> dados.dat
done
