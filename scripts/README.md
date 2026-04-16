<div align="center">
<h1>README</h1>
</div>

## `qeInputBuilder.py`
Utility script for automated generation of Quantum ESPRESSO (`pw.x`) input
files used in ZnO dataset creation for ANN training. 
It builds anisotropically strained and, optionally, noise-perturbed supercells 
from a primitive ZnO cell and writes valid inputs with consistent naming, 
pseudopotential mapping, and k-point grids.

Uses the __Atomic Simulation Environment (ASE)__ to handle atomic structures, 
lattice transformations, random displacements, and input writing. 

## `aenetpy_post_processing.py` / `aenet_post_processing.py`

Post-processing helper for ænet-PyTorch/aenet training and prediction outputs. It
parses `train.error`/`train.out`, `predict.out`, and ZnO `.xsf` files to build Pandas tables
for loss curves, DFT-vs-ANN energy comparison, DFT-vs-ANN force comparison, and
force RMSE values.
