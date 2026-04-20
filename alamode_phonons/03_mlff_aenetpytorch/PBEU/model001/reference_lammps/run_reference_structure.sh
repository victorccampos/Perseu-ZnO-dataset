#!/usr/bin/env bash
set -euo pipefail

LAMMPS_BIN="$HOME/MLFF_AENET-v2.4/lammps-4Feb20/src/lmp_mpi"

INPUT_LMP="in_reference.lmp"
reference_structure="pbeu_supercell.lammps"


"$LAMMPS_BIN" < "$INPUT_LMP" > log.lammps

