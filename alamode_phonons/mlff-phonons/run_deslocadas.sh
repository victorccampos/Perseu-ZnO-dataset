#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

# --- Executável do LAMMPS ---
LAMMPS_BIN="$HOME/MLFF_AENET-v2.4/lammps-4Feb20/src/lmp_mpi"
INPUT_LMP="md.lmp"

mkdir -p xfset

for f in displaced/zno_mlff*.lammps; do
    base=$(basename "$f" .lammps)

    rm -f XFSET tmp.lammps log.lammps
    cp "$f" tmp.lammps

    "$LAMMPS_BIN" < "$INPUT_LMP" > "xfset/log.${base}.lammps"
    mv XFSET "xfset/XFSET.${base}"
done
