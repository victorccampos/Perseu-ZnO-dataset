import os
import numpy as np
from itertools import product

# Atomic Simulation Environment (ASE) imports
from ase.io import read
from ase import Atoms
from ase.build import make_supercell
from ase.io.espresso import write_espresso_in


def get_supercell(
    primitive_cell: Atoms,
    shape: tuple[int, int, int],
    a: float,
    covera: float | None = None,
) -> Atoms:
    """Gera uma nova estrutura a partir da célula primitiva com novos parâmetros de rede"""
    c = a * covera
    new_cell_vec = np.array([[a, 0, 0], [-a / 2.0, a * np.sqrt(3) / 2.0, 0], [0, 0, c]])
    new_prim = Atoms(
        symbols=primitive_cell.get_chemical_symbols(),
        scaled_positions=primitive_cell.get_scaled_positions(),
        cell=new_cell_vec,
        pbc=True,
    )
    supercell = make_supercell(prim=new_prim, P=np.diag(shape))
    # Metadados no obj Atoms
    supercell.info.update(
        {"shape": shape, "prim_a": a, "prim_c": c, "prim_covera": covera}
    )
    return supercell


def setup_strain(value: float) -> np.ndarray:
    """Strain de ±10% em passos de 2%"""
    strain = [0.9, 0.92, 0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06, 1.08, 1.1]
    return value * np.array(strain)


def setup_hubbard(U_Zn: float, U_O: float) -> list[str]:
    qe_hubbard_card = ["HUBBARD (atomic)", f"U Zn-3d {U_Zn}", "U O-2p {U_O}"]
    return qe_hubbard_card


def get_shapes() -> list[tuple]:
    """Retorna as formas únicas de supercélulas considerando a simetria XY."""
    ni = [1, 2, 3]
    # Filtra mantendo nx >= ny e ordena pelo número total de átomos.
    shapes = [shape for shape in product(ni, ni, ni) if shape[0] >= shape[1]]
    return sorted(shapes, key=np.prod)


def write_pwscf(supercell: Atoms, config: dict, noise: float = 0.0) -> None:
    shape_str = "".join(map(str, supercell.info["shape"]))
    a = supercell.info["prim_a"]
    covera = supercell.info["prim_covera"]
    displacements = None

    if noise:
        filename = f"ZnO-{a:.2f}-{covera:.2f}-{shape_str}-{noise}.in"
        seed = np.random.randint(0, int(1e9))
        initial_pos = supercell.get_positions()
        supercell.rattle(noise, seed)
        displacements = supercell.get_positions() - initial_pos

    else:
        filename = f"ZnO-{a:.2f}-{covera:.2f}-{shape_str}.in"

    additional_cards = None
    if config.get("hubbard", False):
        additional_cards = [
            "HUBBARD (atomic)",
            f"U Zn-3d {config.get('U_Zn')}",
            f"U O-2p {config.get('U_O')}",
        ]

    write_espresso_in(
        file=filename,
        atoms=supercell,
        input_data=config["input_data"],
        pseudopotentials=config["pseudos"],
        kpts=config["k_grid"],
        koffset=(0, 0, 0),
        crystal_coordinates=True,
        additional_cards=additional_cards,
    )

    if displacements is not None:
        with open(filename, "a") as f:
            symbols = supercell.get_chemical_symbols()
            f.write("\n! ========================================================\n")
            f.write("! Gaussian random displacements added \n")
            f.write(f"! Random seed = {seed} (std={noise:.3f} Å)\n")
            f.write("! Format: atom_index   symbol   dx   dy   dz   (Å)\n")
            for i, (sym, d) in enumerate(zip(symbols, displacements)):
                f.write(
                    f"! {i + 1:3d}   {sym:2s}   {d[0]: .6f}   {d[1]: .6f}   {d[2]: .6f}\n"
                )
            f.write("! ========================================================\n")

    return


def create_dataset_files(template_path: str, config: dict, noise: float = 0.00) -> None:
    """Gera o dataset de estruturas com deformações e deslocamentos aleatórios para várias supercélulas."""
    prim_cell: Atoms = read(template_path)
    relaxed_a, _, relaxed_c = prim_cell.cell.lengths()

    strains_a = setup_strain(relaxed_a)
    strains_covera = setup_strain(relaxed_c / relaxed_a)

    shapes = get_shapes()
    print(f"{' Iniciando a geração dos arquivos ':=^60}")

    count = 0
    for shape, a, covera in product(shapes, strains_a, strains_covera):
        supercell = get_supercell(prim_cell, shape, a, covera)
        write_pwscf(supercell, config, noise=noise)
        count += 1

    print(
        f"\n Finalizado! {count} arquivos de input do Quantum ESPRESSO foram criados!\n"
    )


if __name__ == "__main__":
    LDA_CONFIG = {
        "control": {
            "calculation": "scf",
            "prefix": "ZnO_LDA",
            "pseudo_dir": "/home/jvc/ZnO_database/pseudos/ppdojo_LDA/",
            "outdir": "./",
            "disk_io": "none",
            "verbosity": "high",
            "tprnfor": True,
        },
        "system": {"ibrav": 0, "ecutwfc": 80, "ecutrho": 320, "occupations": "fixed"},
        "electrons": {"conv_thr": 1.0e-8, "mixing_beta": 0.3},
    }
    qe_config = {
        "input_data": LDA_CONFIG,
        "pseudos": {
            "Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf",
            "O": "O_pseudo-dojo_NC_SR_LDA.upf",
        },
        "k_grid": (6, 6, 4),
        "hubbard": False,
    }

    template = "/home/jvc/ZnO_database/DFT_LDA/02_phonon_DFPT/vcrelax.out"
    create_dataset_files(template_path=template, config=qe_config, noise=0.0)
