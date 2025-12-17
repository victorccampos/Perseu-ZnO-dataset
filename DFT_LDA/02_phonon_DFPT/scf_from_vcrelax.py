from ase.io import read, write
from ase.io.espresso import write_espresso_in
from pathlib import Path
from ase import Atoms
import numpy as np

# GLOBAL CONFIGURATIONS OF SCF'S
CONTROL = {
        "calculation": "scf",
        "prefix": "ZnO_scf",
        "pseudo_dir": "/home/jvc/LDA_Study/pseudos/pseudo_dojo",
        "outdir": "./scf-dump",
        "tprnfor": True,
        "verbosity": "high"
}
SYSTEM = {
    "occupations": "fixed",
    "ecutwfc": 80,
    "ecutrho": 320
}
ELECTRONS = {
    "conv_thr": 1e-8,
    "mixing_beta": 0.3
}
PSEUDOS = {
    "Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf",
    "O": "O_pseudo-dojo_NC_SR_LDA.upf"
}
KPTS = (6, 6, 4)

INPUT_DATA = {
    "control": CONTROL,
    "system": SYSTEM,
    "electrons": ELECTRONS
}

def write_scf_from_vcrelax(vcrelax_output_path, pwi_name: str, add_hubbard = False) -> None:
    """
    Create PWSCF from optimized vc-relax structure.
    
    Sanity test: 
        $ ase convert -i espresso-in ZnO.scf.in ZnO.scf.cif
    """
    atoms: Atoms = read(vcrelax_output_path, format='espresso-out')

    a, b, c, alpha, beta, gamma = atoms.cell.cellpar()
    atomic_positions = atoms.get_scaled_positions()   # [Zn, Zn, O, O]
    symbols: list[str] = atoms.get_chemical_symbols() # ['Zn', 'O']

    print(f"Escrevendo novo scf com configuração relaxada:\n{pwi_name}")
    print(f"\nParâmetros De Rede:\n")
    
    print(f'{a = }')
    print(f'{c = }\n')

    print("Posições Atômicas")
    for sym, pos in zip(symbols, atomic_positions):
        print(f"{sym:2s} {pos[0]: .9f} {pos[1]: .9f} {pos[2]: .9f}")

    write_espresso_in(
        file = pwi_name,
        atoms = atoms,
        input_data = INPUT_DATA, pseudopotentials = PSEUDOS, kpts = KPTS,
        crystal_coordinates=True
    )
    
    if add_hubbard:   
        with open(SCF_INPUTNAME,'a') as f:
            f.write("\nHUBBARD (atomic)\n")
            f.write(f"U Zn-3d 12\n")
            f.write(f"U O-2p 7.0\n")
    
    return None

if __name__ == "__main__":
    vcrelax_path = "./vcrelax.out" 
    pwi_name: str = "ZnO.scf.in"
    write_scf_from_vcrelax(vcrelax_path, pwi_name, add_hubbard=False)
    