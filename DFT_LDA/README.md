# System Preparation for LDA description of Zinc-Oxide


## Objective

Before generating a high-throughput dataset for machine learning, it is essential to validate the computational parameters and characterize the system. This phase includes:

- Convergence tests (ecut, k-point grid)
- Structural relaxation
- Electronic structure analysis (band structure, DOS)

## Directory Structure

./
├── ecut_convergence/ # Total energy vs. plane-wave cutoff
├── k_convergence/ # Total energy vs. k-point mesh density
├── structural_optimization/ # Atomic relaxation and final structure
├── phonon_bands/ # Band structure calculation
├── eletronic_bands/ # Band structure calculation
└── density_of_states/ # Density of states calculation

- **DFT engine**: Quantum ESPRESSO
- **Pseudopotentials**: Optimized Norm-Conserving Potentials from [pseudo-dojo](https://www.pseudo-dojo.org/) library 
