#!/usr/bin/env bash

# lista explícita da ordem desejada
ordem=(
  111 112 211 113 311 212 221 213 312 321
  222 313 331 223 322 323 332 333
)

for sc in "${ordem[@]}"; do
    for f in ZnO-*-*-"$sc".out; do
        [[ -e "$f" ]] || continue
        tempo=$(grep "^\s*PWSCF" "$f")
        echo "$f: $tempo"
    done
done
echo "Execução concluída."