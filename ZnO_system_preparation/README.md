# System Preparation for ZnO DFT Dataset

This directory contains all the preliminary DFT studies carried out to ensure the physical reliability and numerical convergence of subsequent large-scale simulations used in the construction of the `ZnO_database`.

## Objective

Before generating a high-throughput dataset for machine learning, it is essential to validate the computational parameters and characterize the system. This phase includes:

- Convergence tests (ecut, k-point grid)
- Structural relaxation
- Electronic structure analysis (band structure, DOS)
- Benchmarking with different processor counts for computational efficiency

## Directory Structure

system_preparation/
├── ecut_convergence/ # Total energy vs. plane-wave cutoff
├── k_convergence/ # Total energy vs. k-point mesh density
├── benchmark_perseu/ # Performance tests for parallel scalability
├── relaxation/ # Atomic relaxation and final structure
├── band_structure/ # Band structure calculation
└── dos/ # Density of states calculation


## Software & Tools

- **DFT engine**: Quantum ESPRESSO
- **Pseudopotentials**: Ultrasoft PseudoPotentials, Funciontal PBE.
- **Visualization tools**: Xcrysden,Atomic Simulation Enviroment , Matplotlib.

## Notes

- All calculations used the same pseudopotential set and XC functional for consistency.
- Smearing type, convergence thresholds, and other input details are documented in the individual subdirectories.
- The results from these tests were used to define standardized parameters (ecut, k-grid, relaxed structure) applied in the `ZnO_database/` dataset generation.

## Authors / Contributions

- João Victor Campos Costa
- Gabriel Bruno de Souza
- Von Braun Nascimento.

## Date

- Start: [2025-04-07]
- Completion: [YYYY-MM-DD]
