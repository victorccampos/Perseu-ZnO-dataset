import os
import json
import numpy as np
from typing import Tuple

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

def make_scf_from_template(a: float, covera: float, supercell_size: Tuple[int, int, int],
    template_path: str = 'ZnO_template.in',
    add_noise: bool = False,
    noise_stdev: float = 0.015,
    directory_mode: bool = True
    ) -> None:
    """Create a supercell input file for Quantum ESPRESSO based on an existing input file.

    Args:
        a : lattice paremeter in Angstrom
        covera: ratio c/a
        supercell_size: diagonal matrix 
        noise_stdev: Desloca os átomos com uma distribuição gaussiana cujo desvio padrão é de noise_stdev Å

        For more info about random displacement: https://ase-lib.org/_modules/ase/atoms.html#Atoms.rattle
    """
    primitive_cell_template = read(template_path, format='espresso-in')
    
    # CELL_PARAMETERS (v1,v2,v3)
    c = a * covera
    new_cell_vectors = [
        [a, 0, 0],
        [-a/2.0, a*(np.sqrt(3)/2.0), 0 ], 
        [0, 0, c]
    ]
    
    new_cell = Atoms(
        symbols = primitive_cell_template.get_chemical_symbols(),
        scaled_positions = primitive_cell_template.get_scaled_positions(),
        cell = new_cell_vectors,
        pbc = True
    )
    nx, ny, nz = supercell_size
    supercell_matrix = np.diag(supercell_size) 
    supercell = make_supercell(prim=new_cell, P=supercell_matrix)
    

    # Directory and files - naming conventions
    directory_name = f'cell{nx}{ny}{nz}.in'
    input_name: str = f'ZnO-{a:.2f}-{covera:.2f}-{nx}{ny}{nz}.in'
    
    is_noisy: bool = add_noise and noise_stdev > 0
    random_seed = np.random.randint(0, 1e9) 

    if is_noisy:
        directory_name = f'random_cell{nx}{ny}{nz}-{noise_stdev}.in'
        input_name = f'ZnO-{a:.2f}-{covera:.2f}-{nx}{ny}{nz}-{noise_stdev}.in' 
        filepath = os.path.join(directory_name, input_name)       
        supercell.rattle(stdev=noise_stdev, seed=random_seed)

    if directory_mode:
        os.makedirs(directory_name, exist_ok=True)
        filepath = os.path.join(directory_name, input_name)
    else:
        filepath = input_name # ".in" created in current directory `scripts`
    
    # Input SCF Quantum Espresso.
    # Namelists
    prefix_qe = input_name.replace(".in", "")
    HEADER_INPUT = read_header_json()
    HEADER_INPUT['control']['prefix'] = prefix_qe
    HEADER_INPUT['control']['tprnfor'] = True
    # Cards
    PSEUDOS = {'Zn': 'Zn.upf','O': 'O.upf'}
    K_GRID = (6, 6, 6) 
    
    write_espresso_in(
        file = filepath,
        atoms = supercell,
        input_data = HEADER_INPUT,
        pseudopotentials = PSEUDOS,
        kpts = K_GRID,
        koffset = (0,0,0),
        crystal_coordinates = True
    )

if  __name__ == "__main__":
    strain_percent_range = np.arange(start= -0.10, stop=0.12, step=0.02) # [start,stop)
    NOISE_LEVEL = 0.05

    
    # ======= Relaxed structure parameters for ZnO ======= # 
    celldm1_bohr = 6.178_821_408_099_141
    celldm1_angstroms = celldm1_bohr * 0.52918
    celldm3 = 1.614_358_356_153_010
    
    print(f"Lattice Parameters from vcrelax2.out:\n")
    print(f"\t a = {celldm1_bohr:.5f} (a.u) = {celldm1_angstroms:.5f} Å ")
    print(f"\t c/a = {celldm3:.5f}\n")
    print("="*120)
    
    # Anistropic Strain - independent values (a, c/a)
    strained_a_values = celldm1_angstroms * (1 + strain_percent_range)
    strained_covera_values = celldm3 * (1 + strain_percent_range)
    
    print("Strained a values:\n", [f"{valor:.5f}" for valor in strained_a_values])
    print()
    print("Strained c/a values:\n", [f"{valor:.5f}" for valor in strained_covera_values])
    print("="*120)
    
    
    # for a in strained_a_values:
    #    for covera in strained_covera_values:
    #        make_scf_from_template(a, covera, supercell_size=(2, 2, 3))

    # make_scf_from_template(
    #                 a=celldm1_angstroms,
    #                 covera=celldm3,
    #                 supercell_size=(1,1,1),
    #                 directory_mode = True,
    #                 add_noise=True
    #             )
