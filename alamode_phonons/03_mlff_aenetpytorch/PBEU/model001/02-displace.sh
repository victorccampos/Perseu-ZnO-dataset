#!/bin/bash


lammps_supercell="pbeu_supercell.lammps"
prefix="pbeu_disp"
pattern_file="pbeu_mlff.pattern_HARMONIC"

displace="$HOME/alamode/tools/displace.py"


conda run -n "alamode" python "$displace" --LAMMPS="$lammps_supercell" --mag=0.01 --prefix "$prefix" -pf "$pattern_file" > "02-displace.out"
