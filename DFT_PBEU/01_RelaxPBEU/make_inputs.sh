#!/usr/bin/env bash

# Gera inputs de vc-relax com varredura de Hubbard U (Zn-3d e O-2p)
# com base no arquivo template 'vcrelax_template.in' (PBE).

BASE_DIR=$(pwd)
TEMPLATE_FILE="vcrelax_template.in"
WORKDIR="vcrelax-files"


U_START=4.00
U_END=12.00
U_STEP=0.50

# Verificar se o arquivo template existe
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Erro: Arquivo template $TEMPLATE_FILE não encontrado!"
    exit 1
fi

mkdir -p "$WORKDIR"

echo "Gerando inputs Hubbard U..."
echo "U_Zn: ${U_START} - ${U_END} (passo ${U_STEP})"
echo "U_O : ${U_START} - ${U_END} (passo ${U_STEP})"
echo "Saída: ${WORKDIR}/"
echo ""

COUNT=0

for U_Zn in $(seq "$U_START" "$U_STEP" "$U_END"); do
  for U_O in $(seq "$U_START" "$U_STEP" "$U_END"); do

    U_Zn_FORMATTED=$(printf "%.2f" "$U_Zn")
    U_O_FORMATTED=$(printf "%.2f" "$U_O")

    INPUT_FILE="ZnO-PBEU-${U_Zn_FORMATTED}_${U_O_FORMATTED}.in"
    INPUT_PATH="${WORKDIR}/${INPUT_FILE}"

    echo "Gerando: ${INPUT_FILE}"

    cat > "$INPUT_PATH" << EOF
$(cat "$TEMPLATE_FILE")

HUBBARD (atomic)
U Zn-3d ${U_Zn_FORMATTED}
U O-2p ${U_O_FORMATTED}
EOF

    COUNT=$((COUNT + 1))
  done
done

echo ""
echo "Inputs gerados: $COUNT"
