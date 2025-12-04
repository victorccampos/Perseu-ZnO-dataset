#!/bin/bash

# Script para rodar vc-relax com varredura de parâmetros Hubbard U
# Valores de U: 4.00 a 12.00 eV em passos de 0.5 (289 combinações)

# Número de processos MPI
NP=16

# Executável do Quantum ESPRESSO
PW_EXEC="$HOME/pw_intel.x"

# Diretório base
BASE_DIR=$(pwd)

# Template file
TEMPLATE_FILE="vcrelax_template.in"

# Verificar se o arquivo template existe
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Erro: Arquivo template $TEMPLATE_FILE não encontrado!"
    exit 1
fi

# Criar diretório para outputs
mkdir -p hubbard_scans

echo "Iniciando varredura de parâmetros Hubbard U..."
echo "Range: U_Zn = 4.00 - 12.00 eV, U_O = 4.00 - 12.00 eV"
echo "Passo: 0.25 eV"
echo ""

# Contador de jobs
COUNT=0

# Loop para U_Zn
for U_Zn in $(seq 9.50 0.50 12.00); do
    # Loop para U_O
    for U_O in $(seq 4.00 0.50 12.00); do

        # Formatar os valores com 2 casas decimais
        U_Zn_FORMATTED=$(printf "%.2f" $U_Zn)
        U_O_FORMATTED=$(printf "%.2f" $U_O)
        
        # Nome do arquivo de input
        INPUT_FILE="zno_vcrelax_hubbard_${U_Zn_FORMATTED}_${U_O_FORMATTED}.in"
        OUTPUT_FILE="zno_vcrelax_hubbard_${U_Zn_FORMATTED}_${U_O_FORMATTED}.out"
        
        # Caminho completo
        INPUT_PATH="hubbard_scans/${INPUT_FILE}"
        OUTPUT_PATH="hubbard_scans/${OUTPUT_FILE}"
        
        echo "Gerando input: U_Zn = ${U_Zn_FORMATTED} eV, U_O = ${U_O_FORMATTED} eV"
        
        # Gerar arquivo de input usando cat com heredoc
        cat > "$INPUT_PATH" << EOF
$(cat "$TEMPLATE_FILE")

HUBBARD (ortho-atomic)
U Zn-3d ${U_Zn_FORMATTED}
U O-2p ${U_O_FORMATTED}
EOF
        
        # Executar o cálculo (comentado para teste - descomente para executar)
        echo "Executando cálculo para U_Zn = ${U_Zn_FORMATTED}, U_O = ${U_O_FORMATTED}"
        cd hubbard_scans
        mpirun -np $NP $PW_EXEC < $INPUT_FILE > $OUTPUT_FILE 2>&1
        cd ..
        
        COUNT=$((COUNT + 1))
        echo "Job $COUNT concluído: $INPUT_FILE"
        echo "---"
    done
done

echo ""
echo "Varredura completa!"
echo "Total de cálculos executados: $COUNT"
echo "Arquivos salvos em: hubbard_scans/"
echo ""
