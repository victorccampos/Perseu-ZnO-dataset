from pathlib import Path

# Atomic Simulation Environment
from ase import Atoms
from ase import io

import numpy as np


def make_bn_zno(a: float, c: float) -> Atoms:
    """Produz um ZnO na fase h-BN (BN-ZnO)"""
    if a <= 0 or c <= 0:
        raise ValueError("Lattice parameters must be positive (a > 0, c > 0).")
    #  Vetores de rede Hexagonal
    a1 = [a, 0, 0]
    a2 = [-a / 2.0, (np.sqrt(3) / 2) * a, 0]
    a3 = [0, 0, c]
    cell = np.array([a1, a2, a3], dtype=float)

    # Coordenadas Fracionárias
    zn1 = (1.0 / 3.0, 2.0 / 3.0, 1.0 / 4.0)
    zn2 = (2.0 / 3.0, 1.0 / 3.0, 3.0 / 4.0)

    # O
    o1 = (1.0 / 3.0, 2.0 / 3.0, 3.0 / 4.0)
    o2 = (2.0 / 3.0, 1.0 / 3.0, 1.0 / 4.0)

    symbols = ["Zn", "Zn", "O", "O"]
    scaled_positions = [zn1, zn2, o1, o2]

    BN_ZnO = Atoms(
        symbols=symbols, scaled_positions=scaled_positions, cell=cell, pbc=True
    )
    return BN_ZnO


if __name__ == "__main__":
    input_data = {
        "control": {
            "calculation": "relax",
            "prefix": "zno_bn_LDA",
            "pseudo_dir": "/home/jvc/ZnO_database/pseudos/ppdojo_LDA/",
            "outdir": "./",
            "verbosity": "high",
            "tprnfor": True,
            "tstress": True,
            "disk_io": "none",
        },
        "system": {
            "ibrav": 0,
            "ecutwfc": 80,
            "ecutrho": 320,
            "occupations": "fixed",
            "nbnd": 32,  # 26 bandas + 6 vazias
        },
        "electrons": {"conv_thr": 1.0e-8, "mixing_beta": 0.3},
    }

    pseudos = {"Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf", "O": "O_pseudo-dojo_NC_SR_LDA.upf"}

    kpts = (6, 6, 4)

    amin = 2.90
    amax = 3.70

    cmin = 3.70
    cmax = 4.50
    step = 0.05  # in Angstroms

    Na = int(round((amax - amin) / step)) + 1
    Nc = int(round((cmax - cmin) / step)) + 1

    a_values = np.linspace(amin, amax, Na)
    c_values = np.linspace(cmin, cmax, Nc)

    images: list[Atoms] = []
    for a in a_values:
        for c in c_values:
            atoms = make_bn_zno(a, c)
            images.append(atoms)

    print(f"{a_values.size = }")
    print(f"{c_values.size = }")

    jobdir = Path("scan_ac")
    jobdir.mkdir(exist_ok=True)

    for atom in images:
        a, b, c = atom.cell.lengths()
        io.write(
            jobdir / f"bn-zno-{a:.2f}-{c:.2f}.in",
            atom,
            pseudopotentials=pseudos,
            input_data=input_data,
            kpts=kpts,
            format="espresso-in",
            crystalcoordinates=True
        )