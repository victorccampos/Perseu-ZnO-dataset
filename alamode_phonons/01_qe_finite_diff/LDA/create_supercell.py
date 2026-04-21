from ase import io
import ase.units as units
from ase import Atoms


# python create_supercell.py >> 01-alm-suggest.in


def write_qe(filename: str, atoms: Atoms, inp_data: dict, pseudos: dict, kpts: tuple):
    io.espresso.write_espresso_in(
        file=filename,
        atoms=atoms,
        input_data=inp_data,
        pseudopotentials=pseudos,
        kpts=kpts,
        koffset=(0, 0, 0),
        crystal_coordinates=True,
    )


if __name__ == "__main__":
    template = "/home/jvc/ZnO_database/DFT_LDA/02_phonon_DFPT/vcrelax.out"

    atoms_primitve = io.read(template)
    lengths = atoms_primitve.cell.lengths()

    print("CELL VECTORS (angstrom)\n")
    for i, vec in enumerate(atoms_primitve.cell):
         print(f"v{i + 1}: {vec}")

    print(f"{'ALAMODE FORMATTED':=^100}")
    print("CELL VECTORS / a \n")
    print(f"a = {lengths[0]} (angstrom)")
    print(f"a = {lengths[0] / units.Bohr} (Bohr)")
    print(f"2a: {(lengths[0] / units.Bohr) * 2} (Bohr) [SUPERCELL 2X2X2]")

    for i, vec in enumerate(atoms_primitve.cell):
        print(f"a{i + 1}: {vec / lengths[0]}")

    sc222 = atoms_primitve.repeat((2, 2, 2))
    scaled_pos = sc222.get_scaled_positions()
    atomic_symbols = sc222.get_chemical_symbols()

    for sym, pos in zip(atomic_symbols, scaled_pos):
        if sym == "Zn":
            sym = "1"
        else:
            sym = "2"
        print(sym, *pos)

    # Writing QE input file.
    filename = "scf-222.pwi"
    LDA_CONFIG = {
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
        "electrons": {"conv_thr": 1.0e-8, "mixing_beta": 0.3},
    }
    pseudos = {
        "Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf",
        "O": "O_pseudo-dojo_NC_SR_LDA.upf",
    }
    kpts = (6, 6, 4)
#    write_qe(filename, atoms=sc222, inp_data=LDA_CONFIG, pseudos=pseudos, kpts=kpts)
