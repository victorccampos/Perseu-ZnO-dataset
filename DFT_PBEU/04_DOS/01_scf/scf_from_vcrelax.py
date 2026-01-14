from ase import Atoms
from ase.io import read
from ase.io.espresso import write_espresso_in
from pathlib import Path


def print_cell_infos(atoms: Atoms) -> None:
    a, b, c, alpha, beta, gamma = atoms.cell.cellpar()
    pos = atoms.get_scaled_positions()
    sym = atoms.get_chemical_symbols()

    print("Parâmetros de rede relaxados:")
    print(f"{a= }")
    print(f"{c= }\n")

    print("Posições atômicas")

    for s, p in zip(sym, pos):
        print(f"{s:2s} {p[0]: .9f} {p[1]: .9f} {p[2]: .9f}")

    vol_per_atoms = atoms.get_volume() / len(atoms)
    print(f"Volume/ Nat = {vol_per_atoms:.6f}\n")


def create_scf(
    vcrelax_path: str, scf_name: str = "ZnO.scf.in", include_U: bool = False
) -> None:
    atoms = read(vcrelax_path, format="espresso-out")

    # ===================== QUANTUM ESPRESSO SETUP ============================#
    CONTROL = {
        "calculation": "scf",
        "prefix": "ZnO_PBEU",
        "pseudo_dir": "/home/jvc/ZnO_database/pseudos/ppdojo_PBE",
        "outdir": "../tmp_qe",
        # "disk_io": "none",
        "tprnfor": True,
        "verbosity": "high",
    }
    SYSTEM = {"occupations": "fixed", "ecutwfc": 80, "ecutrho": 320, "nbnd": 36}
    ELECTRONS = {"conv_thr": 1e-8, "mixing_beta": 0.3}

    PSEUDOS = {"Zn": "Zn_ppdojo_SR_NC_PBE.upf", "O": "O_ppdojo_SR_NC_PBE.upf"}
    KPTS = (6, 6, 4)

    INPUT_DATA = {"control": CONTROL, "system": SYSTEM, "electrons": ELECTRONS}
    # =========================================================================#

    write_espresso_in(
        file=scf_name,
        atoms=atoms,
        input_data=INPUT_DATA,
        pseudopotentials=PSEUDOS,
        kpts=KPTS,
        crystal_coordinates=True,
    )
    prepend_header_to_file(scf_name, vcrelax_path)

    if include_U:
        add_hubbard(scf_name, U_Zn=9.50, U_O=7.50)

    return None


def prepend_header_to_file(scf_file: str, vcrelax_path: str) -> None:
    with open(scf_file, "r", encoding="utf-8") as f:
        content = f.read()

    with open(scf_file, "w", encoding="utf-8") as f:
        f.write(f"! Input criado com {Path(__file__).name}.\n")
        f.write(f"! Source: {vcrelax_path}.\n")
        f.write(content)


def add_hubbard(scf_file: str, U_Zn, U_O) -> None:
    hubbard_section = f"\nHUBBARD (atomic)\nU Zn-3d {U_Zn}\nU O-2p {U_O}\n"
    with open(scf_file, "a") as file:
        file.write(hubbard_section)


if __name__ == "__main__":
    vcrelax = "/home/jvc/ZnO_database/DFT_PBEU/01_RelaxPBEU/vcrelax-files/ZnO-PBEU-9.50_7.50.out"

    print(f"PROGRAM: {Path(__file__).name}\n")
    print(
        "Creating self-consistent file of Quantum ESPRESSO from variable cell calculation."
    )
    print(f"Source:\n\t{vcrelax}\n")

    create_scf(vcrelax, include_U=True)
