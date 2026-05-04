import numpy as np
from itertools import product
from ase.io import read
from ase import Atoms
from ase.build import make_supercell
from ase.io.espresso import write_espresso_in


QE_CONFIG = {
    "input_data": {
        "control": {
            "calculation": "scf",
            "prefix": "ZnO_LDA",
            "pseudo_dir": "/home/jvc/ZnO_database/pseudos/ppdojo_LDA/",
            "outdir": "./",
            "disk_io": "none",
            "verbosity": "high",
            "tprnfor": True,
            "tstress": True,
        },
        "system": {"ibrav": 0, "ecutwfc": 80, "ecutrho": 320, "occupations": "fixed"},
        "electrons": {"conv_thr": 1e-8, "mixing_beta": 0.3},
    },
    "pseudos": {
        "Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf",
        "O": "O_pseudo-dojo_NC_SR_LDA.upf",
    },
}


def build_structure(
    ref: Atoms,
    shape: tuple[int, int, int],
    fa: float = 1.0,
    fc: float = 1.0,
    noise: float = 0.0,
    seed: int | None = None,
) -> Atoms:
    """
    Builds a strained supercell with independent a and c strain factors.

      Isotropic   (hydrostatic): fa == fc
      Uniaxial c:                fa=1,  fc≠1
      Biaxial in-plane:          fa≠1,  fc=1
      Mixed:                     fa≠1,  fc≠1
    """
    sc = make_supercell(ref, np.diag(shape))
    cell = sc.cell.array.copy()
    # strain
    cell[:2] *= fa
    cell[2] *= fc
    sc.set_cell(cell, scale_atoms=True)
    sc.info["shape"] = shape
    # random displacements
    if noise > 0.0:
        seed = seed or np.random.randint(int(1e9))
        pos_before = sc.get_positions()
        sc.rattle(stdev=noise, seed=seed)
        sc.arrays["displacements"] = sc.get_positions() - pos_before
        sc.info["rattle_seed"] = seed
        sc.info["rattle_std"] = noise

    return sc


def write_structure(
    sc: Atoms,
    fname: str,
    config: dict,
    base_k: tuple[int, int, int] = (6, 6, 4),
) -> None:
    """Writes a QE input file. base_k is the target grid for the primitive cell."""
    shape = sc.info["shape"]
    kpts = tuple(int(np.ceil(base_k[i] / shape[i])) for i in range(3))
    write_espresso_in(
        fname,
        sc,
        input_data=config["input_data"],
        pseudopotentials=config["pseudos"],
        kpts=kpts,
        koffset=(0, 0, 0),
        crystal_coordinates=True,
    )
    displacements = sc.arrays.get("displacements")

    if displacements is not None:
        # recover info of Atoms.
        seed = sc.info["rattle_seed"]
        std = sc.info["rattle_std"]
        # write table at the end of pwscf
        with open(fname, "a") as f:
            header = f"# {'idx':>4}  {'sym':<3}  {'dx (Å)':>10}  {'dy (Å)':>10}  {'dz (Å)':>10}\n"
            rows = "# {:4d}  {:<3}  {:>10.6f}  {:>10.6f}  {:>10.6f}\n"
            sep = f"# {'─' * 54}\n"

            f.write(sep)
            f.write(f"# Gaussian displacements  seed={seed}  std={std:.3f} Å\n")
            f.write(header)
            for i, (sym, d) in enumerate(zip(sc.get_chemical_symbols(), displacements)):
                f.write(rows.format(i + 1, sym, d[0], d[1], d[2]))
            f.write(sep)

    print(f"{fname}")


def make_fname(shape: tuple, fa: float, fc: float, noise: float) -> str:
    return f"ZnO-{''.join(map(str, shape))}-fa{fa:.2f}-fc{fc:.2f}-n{noise:.3f}.in"


if __name__ == "__main__":
    TEMPLATE = "/home/jvc/ZnO_database/DFT_LDA/02_phonon_DFPT/vcrelax.out"
    NOISES = [0.0]
    STRAIN_A = np.linspace(0.90, 1.10, 11)
    STRAIN_C = np.linspace(0.90, 1.10, 11)
    BASE_K = (6, 6, 4)

    ref = read(TEMPLATE)

    # Single structure
    sc = build_structure(ref, shape=(2, 2, 1), fa=1.02, fc=0.98)
    write_structure(sc, "ZnO-221-test.in", QE_CONFIG, BASE_K)

    # ── Full dataset ──────────────────────────────────────────────────────────
    # ni = [1, 2, 3]
    # shapes = sorted(
    #     [s for s in product(ni, ni, ni) if s[0] >= s[1] and np.prod(s) <= 10],
    #     key=np.prod,
    # )
    # count = 0
    # for shape, fa, fc, noise in product(shapes, STRAIN_A, STRAIN_C, NOISES):
    #     sc = build_structure(ref, shape, fa, fc, noise)
    #     write_structure(sc, make_fname(shape, fa, fc, noise), QE_CONFIG, BASE_K)
    #     count += 1
    # print(f"\nFinalizado! {count} arquivos gerados.")
