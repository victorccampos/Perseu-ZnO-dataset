import os
import numpy as np
from itertools import product

# Atomic Simulation Environment (ASE) imports
from ase.io import read
from ase import Atoms
from ase.build import make_supercell
from ase.io.espresso import write_espresso_in

from header_input import INPUT_DATA_LDA, INPUT_DATA_PBE


def transform_primitive_cell(
    primitive_cell_template: str,
    supercell_shape: tuple[int, int, int],
    a: float,
    c: float | None = None,
    covera: float | None = None,
) -> Atoms:
    """
    Transform a primitive cell to a supercell for a given size.

    Args:
        primitive_cell_template: path to building block structure
        supercell_shape: final supercell shape (nx, ny, nz)
        a: new lattice parameter a in Angstroms
        c: new lattice parameter c in Angstroms
        covera: new lattice parameter ratio c/a
    """
    primitive_cell: Atoms = read(primitive_cell_template)
    chemical_symbols: list[str] = primitive_cell.get_chemical_symbols()
    scaled_positions: np.ndarray = primitive_cell.get_scaled_positions()

    if (covera is not None) and (c is None):
        c = a * covera
    elif (covera is None) and (c is not None):
        covera = c / a

    elif (covera is None) and (c is None):
        raise ValueError("Provide either covera or c parameters!\n")

    new_cell_vec = np.array(
        [[a, 0, 0], [-a / 2.0, a * (np.sqrt(3) / 2.0), 0], [0, 0, c]]
    )

    primitive_cell = Atoms(
        symbols=chemical_symbols,
        scaled_positions=scaled_positions,
        cell=new_cell_vec,
        pbc=True,
    )
    supercell = make_supercell(primitive_cell, np.diag(supercell_shape))

    # Save supercell metadata to naming inputs
    supercell.info["shape"] = supercell_shape
    supercell.info["prim_a"] = a
    supercell.info["prim_c"] = c
    supercell.info["prim_covera"] = covera

    return supercell


def prepend_hubbard_block(filepath, U_Zinc, U_Oxygen):
    with open(filepath, "a") as f:
        f.write("\nHUBBARD (atomic)\n")
        f.write(f"U Zn-3d {U_Zinc}\n")
        f.write(f"U O-2p {U_Oxygen}\n")


def build_io_names(
    supercell: Atoms, noise_level = 0, num_structure: int | None = None
) -> tuple[str, str]:
    """
    Args:
        supercell     - the ASE object representing the structure
        noise_level   - gaussian noise in atomic positions (sigma)
        num_structure - a free index to store the structure number
        when we want,
    """
    # Structural parameters of Atoms obj to name inputs
    nx, ny, nz = supercell.info["shape"]

    # Modified Lattice Parameters as fallback values.
    lattice_params = supercell.cell.cellpar()
    a = lattice_params[0]
    c = lattice_params[2]
    covera = c / a

    prim_a = supercell.info.get("prim_a", a)
    prim_covera = supercell.info.get("prim_covera", covera)

    # Default (no-noise)
    directory_name = f"cell_{nx}{ny}{nz}.in"
    input_name: str = f"ZnO-{prim_a:.2f}-{prim_covera:.2f}-{nx}{ny}{nz}.in"

    if noise_level != 0:
        directory_name = f"random_{nx}{ny}{nz}.in"
        input_name = f"ZnO-{prim_a:.2f}-{prim_covera:.2f}-{noise_level}-{nx}{ny}{nz}.in"

    if num_structure is not None:
        input_name = (
            f"ZnO-{prim_a:.2f}-{prim_covera:.2f}-"
            f"{noise_level}-{num_structure}-"
            f"{nx}{ny}{nz}.in"
        )
    return directory_name, input_name


def setup_strain(relaxed_lattice_param: float) -> np.ndarray:
    """Apply small strain to a given lattice parameter. Range from -5% to +5% in
    steps of 1%."""
    range_in_percert = 5
    step = 1
    strain = 1 + np.arange(-range_in_percert, range_in_percert + step, step) / 100
    strained_values = relaxed_lattice_param * strain
    return strained_values


def get_shapes() -> list[np.ndarray]:
    ni_values = [1, 2, 3]
    # Combinações (nx, ny, nz)
    combinations = [
        np.array([nx, ny, nz])
        for nx, ny, nz in product(ni_values, ni_values, ni_values)
        if nx >= ny  # condição de simetria reduzida
    ]

    # ordena pela multiplicidade (número de átomos)
    combinations.sort(key=lambda x: np.prod(x))
    print(
        f"{'Unique supercells shapes considering XY symmetry':_^150}\n", *combinations
    )
    return combinations


def write_pwscf(
    config: dict,
    supercell: Atoms,
    noise_level=0,
    num_structure=None,
    create_dir=True,
    add_U=False,
) -> None:
    # IO
    directory_name, input_name = build_io_names(supercell, noise_level, num_structure)
    displacements, random_seed = None, None

    if noise_level:
        random_seed = np.random.randint(0, 1e9)
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
    print(f"Writing {filepath}")
    write_espresso_in(
        file=filepath,
        atoms=supercell,
        input_data=config["input_data"],
        pseudopotentials=config["pseudos"],
        kpts=config["k_grid"],
        koffset=(0, 0, 0),
        crystal_coordinates=True,
    )

    if add_U:
        prepend_hubbard_block(filepath, U_Zinc=9.5, U_Oxygen=7.5)

    if displacements is not None:
        symbols = supercell.get_chemical_symbols()

        SEP = "\n! ========================================================\n"
        TITLE = "! Gaussian random displacements added \n"
        SEED_LINE = f"! Random seed = {random_seed} (std={noise_level:.3f} Å)\n"
        COLS_LABELS = "! Format: atom_index   symbol   dx   dy   dz   (Å)\n"

        with open(filepath, "a") as f:
            f.write(SEP)
            f.write(TITLE)
            f.write(SEED_LINE)
            f.write(COLS_LABELS)
            for i, (sym, d) in enumerate(zip(symbols, displacements)):
                LINE = f"! {i + 1:3d}   {sym:2s}   {d[0]: .6f}   {d[1]: .6f}   {d[2]: .6f}\n"
                f.write(LINE)
            f.write(SEP)

    return

def create_dataset_files(primitive_cell_template: str, config_dict) -> None:
    """
    Create a dataset of Quantum ESPRESSO input files by applying strains to a primitive cell.
    This function reads a primitive cell structure from a file, applies a range of strains to the lattice parameters,
    and generates supercells for different shapes and strain values. Also, it is possible to add random displacemens.
    For each combination, it writes a Quantum ESPRESSO input file using the provided configuration.
    Args:
        primitive_cell_template (str): Path to the file containing the primitive cell structure.
        config_dict (dict): Configuration dictionary for Quantum ESPRESSO input generation.
    Returns: None
        - Writes Quantum ESPRESSO input files to disk for each generated supercell.
        - Prints the total number of input files created.
    """
    relaxed_structure: Atoms = read(primitive_cell_template)
    relaxed_a = relaxed_structure.cell.lengths()[0]
    relaxed_c = relaxed_structure.cell.lengths()[2]
    relaxed_covera = relaxed_c / relaxed_a

    strained_a_values = setup_strain(relaxed_a)
    strained_covera_values = setup_strain(relaxed_covera)
    shapes = get_shapes()
    
    # main loop
    for shape in shapes:
        for a in strained_a_values:
            for covera in strained_covera_values:
                supercell = transform_primitive_cell(primitive_cell_template,shape,a=a, covera=covera)
                write_pwscf(config=config_dict, supercell=supercell.copy(), noise_level=0.01, create_dir=False)
    
    print("Done!\n")
    NUM_INPUTS = len(shapes) * len(strained_a_values) * len(strained_covera_values)
    print(f"{NUM_INPUTS} Quantum ESPRESSO input files created.\n")
    return None

if __name__ == "__main__":
    """
    LDA or PBE setup
    """
    # ---
    # LDA
    primitive_cell_template = (
        "/home/jvc/ZnO_database/DFT_LDA/02_phonon_DFPT/vcrelax.out"
    )
    INPUT_DATA = INPUT_DATA_LDA # &control &system &electrons
    PSEUDOS_LDA = {
        "Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf",
        "O": "O_pseudo-dojo_NC_SR_LDA.upf"
    }
    K_GRID = (6, 6, 4)
    qe_config = {"input_data": INPUT_DATA, "k_grid": K_GRID, "pseudos": PSEUDOS_LDA}
    create_dataset_files(primitive_cell_template, qe_config)