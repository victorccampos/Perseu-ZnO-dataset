from pathlib import Path
import numpy as np

from ase import Atoms
from ase.io import write

import ase.units as units


def hexagonal_cell(a: float, c: float) -> np.ndarray:
    cell = np.array(
        [
            [a, 0.0, 0.0],
            [-0.5 * a, 0.5 * np.sqrt(3.0) * a, 0.0],
            [0.0, 0.0, c],
        ]
    )
    return cell


def build_h_zno(a: float, c: float) -> Atoms:
    """Example h-ZnO with 4 atoms in order: Zn, Zn, O, O"""

    cell: np.ndarray = hexagonal_cell(a, c)

    # Example fractional coordinates
    # Edit these to match
    scaled_positions = [
        [0.6666666667, 0.3333333333, 0.44],  # Zn
        [0.3333333333, 0.6666666667, 0.94],  # Zn
        [0.6666666667, 0.3333333333, 0.94],  # O
        [0.3333333333, 0.6666666667, 0.44],  # O
    ]
    atoms = Atoms(
        symbols=["Zn", "Zn", "O", "O"],
        scaled_positions=scaled_positions,
        cell=cell,
        pbc=True,
    )
    return atoms


def write_qe_relax_input(
    atoms: Atoms,
    filename: str = "relax_hzno.in",
    pseudo_dir: str = "/home/jvc/LDA_Study/pseudos/pseudo_dojo",
    prefix: str = "hZnO_relax_LDA",
):
    """
    Write a QE relax input using ASE (ibrav=0).
    """

    input_data = {
        "control": {
            "calculation": "relax",
            "prefix": prefix,
            "outdir": "./",
            "pseudo_dir": pseudo_dir,
            "nstep": 300,
            "tstress": True,
            "tprnfor": True,
            "etot_conv_thr": 1.0e-8,
            "forc_conv_thr": 1.0e-4,
            "verbosity": "high",
            "disk_io": "none",
        },
        "system": {
            "ibrav": 0,
            "nat": len(atoms),
            "ntyp": len(set(atoms.get_chemical_symbols())),
            "ecutwfc": 80,
            "ecutrho": 320,
            "occupations": "fixed",
            "nbnd": 36,
        },
        "electrons": {
            "diagonalization": "david",
            "mixing_mode": "local-TF",
            "conv_thr": 1.0e-12,
            "mixing_beta": 0.3,
            "electron_maxstep": 120,
        },
        "ions": {
            "ion_dynamics": "bfgs",
        },
    }

    pseudopotentials = {
        "Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf",
        "O": "O_pseudo-dojo_NC_SR_LDA.upf",
    }

    with open(filename, "w") as fd:
        write(
            fd,
            atoms,
            format="espresso-in",
            input_data=input_data,
            pseudopotentials=pseudopotentials,
            kpts=(6, 6, 4),
            koffset=(0, 0, 0),
            crystal_coordinates=True,
        )


if __name__ == "__main__":
    # Tentativa 1
    a_values = [3.00 + 0.05 * i for i in range(0, 11)]
    # c_values = [3.90 + 0.10 * i for i in range(0, 11)]

    # a_values = []
    c_values = [5.00, 5.10, 5.20, 5.30]
    for a in a_values:
        for c in c_values:
            atoms = build_h_zno(a=a, c=c)
            write_qe_relax_input(atoms, filename=f"relax_hzno_{a:.2f}_{c:.2f}.in")
