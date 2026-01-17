#!/usr/bin/env bash

# -----------------------------
# Arquivos de entrada
# -----------------------------
SCF_FILE="ZnO.scf.in"
PH_FILE="ZnO.ph.in"
Q2R_FILE="q2r.in"
MATDYN_FILE="matdyn.in"

echo "========================================"
echo "Início do workflow de fônons"
echo "Data/Hora: $(date)"
echo "Diretório: $(pwd)"
echo "========================================"
echo

# -----------------------------
# SCF
# -----------------------------
echo ">>> SCF iniciado em: $(date)"
mpirun -np 16 pw.x < "$SCF_FILE" > "${SCF_FILE%.in}.out"
echo ">>> SCF finalizado em: $(date)"
echo

# -----------------------------
# PH
# -----------------------------
echo ">>> PH iniciado em: $(date)"
mpirun -np 16 ph.x < "$PH_FILE" > "${PH_FILE%.in}.out"
echo ">>> PH finalizado em: $(date)"
echo

# -----------------------------
# Q2R
# -----------------------------
echo ">>> Q2R iniciado em: $(date)"
q2r.x < "$Q2R_FILE" > "${Q2R_FILE%.in}.out"
echo ">>> Q2R finalizado em: $(date)"
echo

# -----------------------------
# MATDYN
# -----------------------------
echo ">>> MATDYN iniciado em: $(date)"
matdyn.x < "$MATDYN_FILE" > "${MATDYN_FILE%.in}.out"
echo ">>> MATDYN finalizado em: $(date)"
echo

echo "========================================"
echo "Cálculo de Fônons FINALIZADO"
echo "Data/Hora: $(date)"
echo "========================================"

