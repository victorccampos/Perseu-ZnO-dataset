#!/usr/bin/env bash

NP=32
PW_EXEC="pw.x"
WORKDIR="vcrelax-files"

for INPUT_PATH in "$WORKDIR"/*.in; do
  INPUT_FILE=$(basename "$INPUT_PATH")
  OUTPUT_FILE="${INPUT_FILE%.in}.out"

  echo "Rodando: $INPUT_FILE -> $OUTPUT_FILE"

  (
    cd "$WORKDIR"
    mpirun -np "$NP" "$PW_EXEC" < "$INPUT_FILE" > "$OUTPUT_FILE" 2>&1
  )
done
echo "Todos os cálculos concluídos."