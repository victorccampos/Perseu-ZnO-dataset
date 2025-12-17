from ase.io import read, write
from ase.io.espresso import write_espresso_in
from pathlib import Path
import numpy as np


# Lê estrutura relaxada.
atoms = read('vcrelax.out', format='espresso-out')


a, b, c, alpha, beta, gamma = atoms.cell.cellpar()

atomic_positions = atoms.get_scaled_positions()

symbols: list[str] = atoms.get_chemical_symbols()

vol_per_atoms = atoms.get_volume()/ len(atoms)


print(f"\nParâmetros de rede relaxados:\n")
print(f'{a= }')
print(f'{c= }\n')

print("Posições atômicas")
for sym, pos in zip(symbols, atomic_positions):
    print(f"{sym:2s} {pos[0]: .9f} {pos[1]: .9f} {pos[2]: .9f}")
print(f"Volume/ Nat = {vol_per_atoms:.6f}\n")

print(f"ESCREVENDO NOVO SCF COM CONFIGURAÇÃO RELAXADA")

# ESCREVENDO NOVO SCF COM CONFIGURAÇÃO RELAXADA
CONTROL = {
    "calculation": "scf",
    "prefix": "ZnO_scf",
    "pseudo_dir": "/home/jvc/LDA_Study/pseudos/pseudo_dojo",
    "outdir": "./out",
    "disk_io": "none",
    "tprnfor": True,
    "tstress": True,
    "verbosity": "high"
}

SYSTEM = {"occupations": "fixed", "ecutwfc": 80, "ecutrho": 320}
ELECTRONS = {"conv_thr": 1e-8, "mixing_beta": 0.3}
PSEUDOS = {"Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf", "O": "O_pseudo-dojo_NC_SR_LDA.upf"}
KPTS = (6, 6, 4)


SCF_INPUTNAME = "ZnO111.scf.in"
write_espresso_in(
     file=SCF_INPUTNAME,
     atoms=atoms,
     input_data={
         "control": CONTROL,
         "system": SYSTEM,
         "electrons": ELECTRONS
     },
     pseudopotentials=PSEUDOS,
     kpts=KPTS,
     crystal_coordinates=True
 )
