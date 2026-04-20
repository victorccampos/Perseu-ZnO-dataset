#!/bin/bash

prefix="zno_lda_mlff"
supercell="ZnO_lda_supercell.lammps"

conda run -n alamode python $HOME/alamode/tools/displace.py --LAMMPS="$supercell" --mag=0.01 --prefix "$prefix" -pf zno_lda_mlff.pattern_HARMONIC
