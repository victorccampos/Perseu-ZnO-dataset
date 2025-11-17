import os
import json
import numpy as np

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


def transform_unit_cell(supercell_shape: tuple[int, int, int],
    a: float, c: float | None = None, covera: float | None = None,
    primitive_cell_scf: str = 'ZnO_template.in') -> Atoms:
    """
    Transform a primitive cell to a supercell for a given size. 
    """
    primitive_cell: Atoms = read(primitive_cell_scf, format='espresso-in')
    chemical_symbols: list[str] = primitive_cell.get_chemical_symbols()
    scaled_positions: np.ndarray = primitive_cell.get_scaled_positions()
    
    # User passes (a, c/a)
    if covera is not None and c is None:
        c = a * covera
    # User passes (a, c)
    elif covera is None and c is not None:
        covera = c / a

    elif covera is None and c is None:
        raise ValueError("Provide either covera or c parameters!\n")
   
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

    # Save supercell metadata to naming inputs
    supercell.info['shape'] = supercell_shape
    supercell.info['prim_a'] = a
    supercell.info['prim_c'] = c
    supercell.info['prim_covera'] = covera

    return supercell

def get_namelists_and_cards(input_name: str) -> tuple[dict, dict, tuple]:
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
    noise_level: float = 0.0,
    num_structure: int | None = None,
    create_dir: bool = True
) -> None:
    
    # IO
    directory_name, input_name = build_io_names(supercell, noise_level, num_structure)
    displacements, random_seed = None, None
    
    if noise_level:
        random_seed: int = np.random.randint(0, 1e9)        
        # Store displacements to append as comments in input file
        initial_positions: np.ndarray = supercell.get_positions().copy()
        supercell.rattle(stdev=noise_level, seed=random_seed)
        final_positions: np.ndarray = supercell.get_positions()
        displacements: np.ndarray = final_positions - initial_positions
    
    if create_dir:
        os.makedirs(directory_name, exist_ok=True)
        filepath = os.path.join(directory_name, input_name)
    else:
        filepath = input_name

    # Writing input file.
    NAMELIST, PSEUDOS, K_GRID = get_namelists_and_cards(input_name)
    
    
    write_espresso_in(file = filepath, atoms = supercell,
        input_data = NAMELIST, pseudopotentials = PSEUDOS, kpts = K_GRID,
        koffset = (0,0,0),
        crystal_coordinates = True
    )

    # Hubbar TODO tirar os valores hard-coded.
    Ud = 11.50
    Up = 8.0
    with open(filepath, "a") as f:
        f.write("\nHUBBARD (ortho-atomic)\n")
        f.write(f"U Zn-3d {Ud}\n")
        f.write(f"U O-2p {Up}\n")

    if displacements is not None:
        symbols = supercell.get_chemical_symbols()
        with open(filepath, "a") as f:
            f.write("\n! ========================================================\n")
            f.write(f"! Gaussian random displacements added (std={noise_level:.3f} Å)\n")
            f.write(f"! Random seed = {random_seed}\n")
            f.write("! Format: atom_index   symbol   dx   dy   dz   (Å)\n")
            for i, (sym, d) in enumerate(zip(symbols, displacements)):
                f.write(f"! {i+1:3d}   {sym:2s}   {d[0]: .6f}   {d[1]: .6f}   {d[2]: .6f}\n")
            f.write("! ========================================================\n")

    return

def build_io_names(supercell: Atoms, noise_level: float = 0.0, num_structure: int | None = None) -> tuple[str, str]:
    # Structural parameters of Atoms obj to name inputs
    nx, ny, nz = supercell.info['shape']    
    
    # Modified Lattice Parameters as fallback values.
    lattice_params = supercell.cell.cellpar()
    a = lattice_params[0]
    c = lattice_params[2]
    covera = c/a

    prim_a = supercell.info.get('prim_a', a)
    prim_covera = supercell.info.get('prim_covera', covera)

    # Default (no-noise)
    directory_name = f'cell_{nx}{ny}{nz}.in'
    input_name: str = f'ZnO-{prim_a:.2f}-{prim_covera:.2f}-{nx}{ny}{nz}.in'
    
    if (noise_level != 0):
        directory_name = f'random_{nx}{ny}{nz}.in'
        input_name = f'ZnO-{prim_a:.2f}-{prim_covera:.2f}-{noise_level}-{nx}{ny}{nz}.in'

    if num_structure is not None:
        input_name= (
                f"ZnO-{prim_a:.2f}-{prim_covera:.2f}-"
                f"{noise_level}-{num_structure}-"
                f"{nx}{ny}{nz}.in"
            )
    return directory_name, input_name

def setup_strain_arrays(
    range_in_percent: int,
    step: int,
    relaxed_a: float,
    relaxed_c: float | None = None,
    relaxed_covera: float | None = None
) -> tuple[np.ndarray, np.ndarray]:
    
    strain_in_percents = np.arange(-range_in_percent, range_in_percent+step, step) / 100
    strain = (1 + strain_in_percents)
    
    isotropic_case: bool = relaxed_a is not None and relaxed_c is not None
    anisotropic_case: bool = relaxed_a is not None and relaxed_covera is not None
    
    if isotropic_case: # user passes (a, c) => isotropic Strain
        print(f"Adding Isotropic strain varying both c and a in {range_in_percent}%")
        strained_a = relaxed_a * strain 
        strained_c = relaxed_c * strain
        for a, c, p in zip(strained_a, strained_c, strain_in_percents):
            print(f'a = {a:.2f} | c = {c:.2f} | {p:.1%} |')
        return strained_a, strained_c
    elif anisotropic_case: # User passes (a, c/a) => anisotropic Strain
        print(f"Adding anisotropic strain varying both a and c/a in {range_in_percent}%")
        strained_a = relaxed_a * strain
        strained_covera = relaxed_covera * strain
        for a, covera, p in zip(strained_a, strained_covera, strain_in_percents):
            print(f'a = {a:.2f} | c/a = {covera:.2f} | {p:.1%} |')
        return strained_a, strained_covera
    else:
        raise ValueError("Provide either covera or c parameters!\n")
   
if  __name__ == "__main__":
    # ======= Relaxed structure parameters for ZnO ======= #     
    a_Bohr = 6.178_821_408_099_141
    ratio_ca = 1.614_358_356_153_010
    
    a_angstroms = a_Bohr * Bohr
    c_angstroms = a_angstroms * ratio_ca 

    # CASE: Anisotropic Strain
    # strained_a_values, strained_covera_values = setup_strain_arrays(
    #         relaxed_a = a_angstroms, 
    #         relaxed_covera = ratio_ca,
    #         range_in_percent= 10,
    #         step = 2
    #     )
    
    # CASE: Isotropic Strain
    strained_a_values, strained_c_values = \
        setup_strain_arrays(
            relaxed_a = a_angstroms, 
            relaxed_c = c_angstroms,
            range_in_percent= 10,
            step = 2
        )
    
    # Random Displacements
    noise_level = 0.04
    n_variant_structures = len(noise_levels)
    
    # ======================= Dataset Creation ======================= #
    # supercell_shape = (2, 1, 2)
    # print(f"Creating input files for {supercell_shape}")
    # for a in strained_a_values:
    #     for covera in strained_covera_values:
            
    #         atoms = transform_unit_cell(supercell_shape=supercell_shape, a=a, covera=covera)

    #         # Numerate structures based on noise level
    #         for idx in range(1, n_variant_structures+1):
    #             make_pwscf_from_atoms(
    #                 supercell = atoms.copy(),
    #                 add_noise = True,
    #                 noise_std_dev = noise_levels[idx-1],
    #                 num_structure = idx
    #             )
    # print(f"Input files created.")
    
    # ======================= 1 FILE Creation ======================= #
    supercell_shape = (2, 2, 2)
    supercell = transform_unit_cell(supercell_shape=supercell_shape, a=a_angstroms, c=c_angstroms)
    make_pwscf_from_atoms(supercell, create_dir = False, noise_level=noise_level, num_structure=69)

