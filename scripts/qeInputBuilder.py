"""Utility script for automated generation of Quantum ESPRESSO (`pw.x`) input
files used in ZnO dataset creation for ANN training. 
It builds anisotropically strained and optionally noise-perturbed supercells
from a primitive ZnO cell and writes valid inputs with consistent naming, 
pseudopotential mapping, and k-point grids.

Uses the Atomic Simulation Environment (ASE) to handle atomic structures, latti-
ce transformations, random displacements, and input writing. 
The configuration headers (control, system, electrons) are read from external 
JSON `header_input.json`, ensuring reproducibility and scalability of dataset 
generation.
"""


import os
import json
import numpy as np
from typing import Tuple, Dict, Optional

# Atomic Simulation Environment (ASE) imports
from ase.io import read                         
from ase import Atoms
from ase.build import make_supercell
from ase.io.espresso import write_espresso_in
from ase.units import Bohr

def read_header_json(json_path='header_input.json') -> dict:
    """
    Return a dictionary with namelists (& sections) of pw.x input
    """
    with open(json_path,'r') as f:
        data: dict = json.load(f)
    return data


def transform_unit_cell(supercell_shape: Tuple[int, int, int],
    a: float,
    covera: float,
    template: str = 'ZnO_template.in'
) -> Atoms:
    """
    Transform a primitive cell to a supercell for a given size. 
    """
    primitive_cell: Atoms = read(template, format='espresso-in')
    chemical_symbols: list[str] = primitive_cell.get_chemical_symbols()
    scaled_positions: np.ndarray = primitive_cell.get_scaled_positions()
    
    c = a * covera
    new_cell_vec = np.array([
        [a, 0, 0],
        [-a/2.0, a*(np.sqrt(3)/2.0), 0 ],
        [0, 0, c],
    ])
    
    primitive_cell = Atoms(
        symbols=chemical_symbols, 
        scaled_positions= scaled_positions,
        cell = new_cell_vec,
        pbc=True
    )
    transform_matrix = np.diag(supercell_shape)
    supercell = make_supercell(primitive_cell, transform_matrix)

    # Save supercell dimensions nx, ny, nz in metadata to naming inputs
    supercell.info['shape'] = supercell_shape
    supercell.info['primitive_a'] = a
    supercell.info['primitive_covera'] = covera

    return supercell

def get_qe_params(input_name: str) -> Tuple[dict, dict, tuple]:
    """
    Args:
        input_name: str - name of the input file (e.g. ZnO-3.25-1.61-222.in)
    Returns:
        NAMELIST: dict - dictionary with namelists (& sections) of pw.x input
        PSEUDOS: dict - dictionary with pseudopotentials
        K_GRID: tuple - k-point grid
    """
    prefix = input_name.replace(".in", "")
    
    # Namelists - &control, &system, &electrons
    NAMELIST = read_header_json()
    NAMELIST['control']['prefix'] = prefix
    NAMELIST['control']['tprnfor'] = True
    
    # Cards
    PSEUDOS = {'Zn': 'Zn.upf','O': 'O.upf'}
    K_GRID = (6, 6, 6)

    return NAMELIST, PSEUDOS, K_GRID



def make_pwscf_from_atoms(
    supercell: Atoms,
    create_dir: bool = True,
    add_noise: bool = False,
    noise_std_dev: float = 0.0,
    num_structure: Optional[int] = None,
) -> None:
    
    # Structural parameters of Atoms obj to naming inputs
    nx, ny, nz = supercell.info['shape']
    
    # Fallback values are the trasformed lattice parameters
    params = supercell.cell.cellpar()
    a = params[0]
    c = params[2]
    covera = c/a

    primitive_a = supercell.info.get('primitive_a', a)
    primitive_covera = supercell.info.get('primitive_covera', covera)

    # I/O naming conventions
    directory_name = f'cell_{nx}x{ny}x{nz}.in'
    input_name: str = f'ZnO-{primitive_a:.2f}-{primitive_covera:.2f}-{nx}{ny}{nz}.in'
    
    displacements = None
    random_seed = None
    if (add_noise and noise_std_dev > 0):
        random_seed = np.random.randint(0, 1e9)
        
        # Store displacements to append as comments in input file
        before = supercell.get_positions().copy()
        supercell.rattle(stdev=noise_std_dev, seed=random_seed)
        after = supercell.get_positions()
        displacements = after - before

        directory_name = f'random_{nx}x{ny}x{nz}.in'
        input_name = f'ZnO-{primitive_a:.2f}-{primitive_covera:.2f}-{nx}{ny}{nz}-{noise_std_dev}.in' 
        
        filepath = os.path.join(directory_name, input_name)

    if num_structure is not None:
        basename, suffix = os.path.splitext(input_name)
        input_name = f"{basename}-{num_structure}{suffix}"

    if create_dir:
        os.makedirs(directory_name, exist_ok=True)
        filepath = os.path.join(directory_name, input_name)
    else:
        filepath = input_name

    # Writing input file.
    NAMELIST, PSEUDOS, K_GRID = get_qe_params(input_name)
    
    
    write_espresso_in(
        file = filepath, atoms = supercell,
        input_data = NAMELIST, pseudopotentials = PSEUDOS, kpts = K_GRID,
        koffset = (0,0,0),
        crystal_coordinates = True
    )

    if displacements is not None:
        symbols = supercell.get_chemical_symbols()
        with open(filepath, "a") as f:
            f.write("\n! ========================================================\n")
            f.write(f"! Gaussian random displacements added (std={noise_std_dev:.3f} Å)\n")
            f.write(f"! Random seed = {random_seed}\n")
            f.write("! Format: atom_index   symbol   dx   dy   dz   (Å)\n")
            for i, (sym, d) in enumerate(zip(symbols, displacements)):
                f.write(f"! {i+1:3d}   {sym:2s}   {d[0]: .6f}   {d[1]: .6f}   {d[2]: .6f}\n")
            f.write("! ========================================================\n")

    return

if  __name__ == "__main__":
    # ======= Relaxed structure parameters for ZnO ======= #     
    celldm1_bohr = 6.178_821_408_099_141
    celldm1_angstroms = celldm1_bohr * Bohr
    celldm3 = 1.614_358_356_153_010
    
    # ================ Strain Setup (-10% <= strain <=10%) ============ # 
    # Anistropic: Independent values (a, c/a) # [start,stop)
    strain_percent_range = np.arange(start= -0.10, stop=0.12, step=0.02) 
    strained_a_values = celldm1_angstroms * (1 + strain_percent_range)
    strained_covera_values = celldm3 * (1 + strain_percent_range)
    
    # 3 noises levels for each (a, c/a) combination
    n_variant_structures = 3
    conservative_stdev, typical_stdev, aggressive_stdev = 0.04, 0.06, 0.12
    noise_levels = [conservative_stdev, typical_stdev, aggressive_stdev]
    
    # ======================= Dataset Creation ======================= #
    supercell_shape = (2, 1, 2)
    print(f"Creating input files for {supercell_shape}")
    for a in strained_a_values:
        for covera in strained_covera_values:
            
            atoms = transform_unit_cell(supercell_shape=supercell_shape, a=a, covera=covera)

            # Numerate structures based on noise level
            for idx in range(1, n_variant_structures+1):
                make_pwscf_from_atoms(
                    supercell = atoms.copy(),
                    add_noise = True,
                    noise_std_dev = noise_levels[idx-1],
                    num_structure = idx
                )
    print(f"Input files created.")
    
    # ======================= 1 FILE Creation ======================= #
    supercell_shape = (2, 2, 2)
    a, covera = celldm1_angstroms, celldm3
    atoms = transform_unit_cell(supercell_shape=supercell_shape, a=a, covera=covera)
    
    make_pwscf_from_atoms(supercell = atoms, create_dir = False)
