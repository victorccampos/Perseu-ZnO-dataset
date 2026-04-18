#!/bin/bash

INPUT="scf-664.pwi"
EXEC="pw.x"

# listas de NP e nk compatíveis
NP_LIST=(32 64)

echo "Benchmark QE (scan em NP e nk)"
echo "Input: ${INPUT}"
echo "---------------------------------------"

for NP in "${NP_LIST[@]}"; do

    echo
    echo "===== NP = ${NP} ====="

    # escolher nk compatível com cada NP
    if [ "$NP" -eq 32 ]; then
        NK_LIST=(1 2 4 8)
    elif [ "$NP" -eq 64 ]; then
        NK_LIST=(1 2 4 8)
    fi

    for NK in "${NK_LIST[@]}"; do

        OUT="out_np${NP}_nk${NK}.out"
        TLOG="time_np${NP}_nk${NK}.log"

        echo "==> Rodando NP=${NP}, nk=${NK}"

        /usr/bin/time -f "real %E | cpu %P" \
            mpirun -np ${NP} ${EXEC} -nk ${NK} -in ${INPUT} > "${OUT}" 2> "${TLOG}"

        # extrair linha PWSCF
        WALL=$(grep "PWSCF" "${OUT}" | tail -n 1)

        echo "    ${WALL}"
        echo "    $(cat ${TLOG})"
        echo
    done
done

echo "=========== RESUMO ==========="

for NP in "${NP_LIST[@]}"; do
    if [ "$NP" -eq 32 ]; then
        NK_LIST=(1 2 4 8)
    elif [ "$NP" -eq 64 ]; then
        NK_LIST=(1 2 4 8)
    fi

    echo
    echo "NP = ${NP}"
    for NK in "${NK_LIST[@]}"; do
        OUT="out_np${NP}_nk${NK}.out"
        printf "nk=%-2s  " "${NK}"
        grep "PWSCF" "${OUT}" | tail -n 1
    done
done