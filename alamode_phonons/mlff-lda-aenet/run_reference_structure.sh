#!/usr/bin/env bash
set -euo pipefail

LAMMPS_BIN="$HOME/MLFF_AENET-v2.4/lammps-4Feb20/src/lmp_mpi"
INPUT_LMP="md.lmp"

rm -f XFSET tmp.lammps log.lammps
cp ZnO_supercell.lammps tmp.lammps

"$LAMMPS_BIN" < "$INPUT_LMP" > log.lammps

mv XFSET XFSET.reference
