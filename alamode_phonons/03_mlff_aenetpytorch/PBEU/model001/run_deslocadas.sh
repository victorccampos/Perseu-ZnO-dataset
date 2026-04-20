#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

# --- Executável do LAMMPS ---
LAMMPS_BIN="$HOME/MLFF_AENET-v2.4/lammps-4Feb20/src/lmp_mpi"
INPUT_LMP="in.lmp"

mkdir -p xfset

for f in displaced/*_disp*.lammps; do
    base=$(basename "$f" .lammps)

    rm -f XFSET tmp.lammps log.lammps
    cp "$f" tmp.lammps

    "$LAMMPS_BIN" < "$INPUT_LMP" > "xfset/log.${base}.lammps"
    mv XFSET "xfset/XFSET.${base}"
done


# python $HOME/alamode/tools/extract.py --LAMMPS=pbeu_supercell.lammps --offset=reference_lammps/XFSET_reference xfset/XFSET.pbeu_disp* > XFSET_harmonic