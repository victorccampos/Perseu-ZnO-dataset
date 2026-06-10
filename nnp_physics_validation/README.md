# README

This directory contain some physics validation of the potentials produced
by model006 neural networks.

## Birch-Murnaghan fit $E(V)$

**Theory:** The third-order Birch-Murnaghan isothermal equation of state models the changes in the energy of a crystal lattice upon isotropic compression or expansion. It is derived by expanding the strain energy in terms of the Eulerian strain. Fitting to this equation allows us to extract fundamental mechanical properties of the material at zero temperature, independent of kinetic effects.

**Workflow:**
1. Start with the ground-state relaxed structure obtained from DFT.
2. Apply isotropic scaling to the lattice vectors to generate a set of strained structures (e.g., from $-5\%$ to $+5\%$ of the equilibrium volume).
3. Compute the single-point energy $E(V)$ for each strained structure using the ML potential.
4. Fit the $E(V)$ data points to the Birch-Murnaghan equation to obtain:
    - $V_0$: Equilibrium volume
    - $E_0$: Equilibrium energy
    - $B_0$: Bulk modulus
    - $B'_0$: Pressure derivative of the bulk modulus

## Thermal Expansion

**Theory:** Thermal expansion is fundamentally driven by the anharmonicity of the interatomic potential. In a perfectly harmonic well, the time-averaged interatomic distance remains strictly constant regardless of the temperature. The volumetric thermal expansion coefficient is defined thermodynamically as $\beta = \frac{1}{V} \left( \frac{\partial V}{\partial T} \right)_P$.

**Workflow:**
1. Initialize a sufficiently large supercell to adequately capture long-range phonon modes and minimize finite-size effects.
2. Run Molecular Dynamics (MD) simulations in the NPT ensemble (constant number of particles, pressure, and temperature) across a range of target temperatures.
3. Allow sufficient time for the system to equilibrate at each temperature step.
4. Calculate the time-averaged volume $\langle V \rangle$ over the production run for each temperature.
5. Extract the thermal expansion coefficient by evaluating the derivative of the $\langle V \rangle$ vs $T$ curve.