import os
import json
import numpy as np
from typing import Tuple, Dict

# Atomic Simulation Environment (ASE) imports
from ase.io import read                         
from ase import Atoms
from ase.build import make_supercell
from ase.io.espresso import write_espresso_in

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
    num_structure: int | None = None,
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
    directory_name = f'cell{nx}{ny}{nz}.in'
    input_name: str = f'ZnO-{primitive_a:.2f}-{primitive_covera:.2f}-{nx}{ny}{nz}.in'
    
    if (add_noise and noise_std_dev > 0):
        random_seed = np.random.randint(0, 1e9)
        supercell.rattle(stdev=noise_std_dev, seed=random_seed)
        
        directory_name = f'random_cell{nx}{ny}{nz}.in'
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
    write_espresso_in(file = filepath, atoms = supercell,
        input_data = NAMELIST,
        pseudopotentials = PSEUDOS,
        kpts = K_GRID,
        koffset = (0,0,0),
        crystal_coordinates = True
    )
    return

if  __name__ == "__main__":
    # ======= Relaxed structure parameters for ZnO ======= # 
    
    celldm1_bohr = 6.178_821_408_099_141
    celldm1_angstroms = celldm1_bohr * 0.52918
    celldm3 = 1.614_358_356_153_010
    
    print(f"Lattice Parameters from vcrelax2.out:\n")
    print(f"\t a = {celldm1_bohr:.5f} (a.u) = {celldm1_angstroms:.5f} Å ")
    print(f"\t c/a = {celldm3:.5f}\n")
    print("="*120)
    
    # ================== Strain Setup =================== # 
    # Anistropic Strain => independent values (a, c/a) 
    strain_percent_range = np.arange(start= -0.10, stop=0.12, step=0.05) # [start,stop)
    strained_a_values = celldm1_angstroms * (1 + strain_percent_range)
    strained_covera_values = celldm3 * (1 + strain_percent_range)
    
    # 3 noises levels for each (a, c/a) combination
    n_variant_structures = 3
    conservative_stdev, typical_stdev, aggressive_stdev = 0.04, 0.06, 0.12
    noise_levels = [conservative_stdev, typical_stdev, aggressive_stdev]

    print("\nStrained a values:\n", [f"{valor:.5f}" for valor in strained_a_values])
    print("\nStrained c/a values:\n", [f"{valor:.5f}" for valor in strained_covera_values])
    print("\n"+"="*120)

    for a in strained_a_values:
        for covera in strained_covera_values:
            SUPERCELL_SHAPE = (1, 1, 2)  
            # Creating Atoms ASE object
            atoms = transform_unit_cell(supercell_shape=SUPERCELL_SHAPE, a=a, covera=covera)


            # Opcao com random positions numeradas
            for idx in range(1, n_variant_structures+1):
                make_pwscf_from_atoms(
                    supercell = atoms.copy(),
                    add_noise = True,
                    noise_std_dev = noise_levels[idx-1],
                    num_structure = idx
                )


    
    
    
