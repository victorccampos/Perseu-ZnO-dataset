<div align="center">
<h1>
README
</h1>
</div>

## `qeInputBuilder.py`
Utility script for automated generation of Quantum ESPRESSO (`pw.x`) input
files used in ZnO dataset creation for ANN training. 
It builds anisotropically strained and, optionally, noise-perturbed supercells from a primitive ZnO cell and writes valid inputs with consistent naming, 
pseudopotential mapping, and k-point grids.

Uses the __Atomic Simulation Environment (ASE)__ to handle atomic structures, lattice transformations, random displacements, and input writing. 

The configuration headers (&control, &system, &electrons) are read from external JSON file `header_input.json`.

## `qeRunner.py`

This script manages the parallel execution of Quantum ESPRESSO input files, handling multiple calculations sequentially with specified MPI and OpenMP parallelization settings. It provides command-line interface for customizing the execution parameters and manages input/output file organization.

__Functions__:  
    `__parse_arguments()__`: Parses command-line arguments for customizing the execution.  
    `__run_qe_job():__` Executes a single Quantum ESPRESSO calculation.
    `__main():__` Orchestrates the overall execution flow.

__Command-line Arguments:__  
    __-d, --directory__ : Directory containing input files (default: "SCFs.in")  
    __-np, --num-processes__: Number of MPI processes (_default: 32_)  
    __-nk, --npools__: Number of k-point pools (default: 8)  
    __--start-from__: Start execution from specific input file.  

__Environment Variables:__  
    __OMP_NUM_THREADS:__ Set to 2 if hybrid OpenMP+MPI parallelization is enabled.  
__Returns:__  None  
__Raises:__  
    SystemExit: If directory creation fails or no input files are found
    Various exceptions: Handled within run_qe_job() for individual calculation failures.

---    