# ZnO Phonons Database

This directory contains data and resources related to phonon calculations for ZnO using Quantum ESPRESSO + ALAMODE.

## Contents

1. `alm_suggest.in` $\rightarrow$ ZnO222.pattern_HARMONIC  
    - Suggest the displacements.
2. `displace.py`  $\rightarrow$ dispXX.in
    - Creates QE scf inputs.
3. `extract.py` $\leftarrow$ dispXX.out $\rightarrow$ DFSET_harmonic
    - Extract data from scf calculations
4. `alm_opt.in` $\rightarrow$ ZnO222.xml
    - Creats ZnO222.xml to anphon program to calculate __phonon dispersion__.  
5. `anphon.in` $\rightarrow$ __ZnO222.bands__


# Exp. Data

`phonon-experimental-data-meV` : experimental data extracter from
_Dielectric properties and Raman spectra of ZnO from a first principles finite-differences/finite-fields approach_

`phonon-experimental-data-THz`: _Thermal Conductivity of Wurtzite Zinc-Oxide from First-Principles Lattice Dynamics - A Comparative Study with Gallium Nitride_
