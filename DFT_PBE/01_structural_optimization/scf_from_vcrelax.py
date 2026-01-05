from ase.io import read
from ase.io.espresso import write_espresso_in


# Lê estrutura relaxada.
atoms = read("vcrelax.out", format="espresso-out")


a, b, c, alpha, beta, gamma = atoms.cell.cellpar()

atomic_positions = atoms.get_scaled_positions()

symbols: list[str] = atoms.get_chemical_symbols()

vol_per_atoms = atoms.get_volume() / len(atoms)


print("\nParâmetros de rede relaxados:\n")
print(f"{a= }")
print(f"{c= }\n")

print("Posições atômicas")
for sym, pos in zip(symbols, atomic_positions):
    print(f"{sym:2s} {pos[0]: .9f} {pos[1]: .9f} {pos[2]: .9f}")
print(f"Volume/ Nat = {vol_per_atoms:.6f}\n")

print("ESCREVENDO NOVO SCF COM CONFIGURAÇÃO RELAXADA")

# ESCREVENDO NOVO SCF COM CONFIGURAÇÃO RELAXADA
CONTROL = {
    "calculation": "scf",
    "prefix": "ZnO_PBE",
    "pseudo_dir": "/home/jvc/ZnO_database/pseudos/ppdojo_PBE",
    "outdir": "../temp-qe",
    "disk_io": "none",
    "tprnfor": True,
    "tstress": True,
    "verbosity": "high",
}

SYSTEM = {"occupations": "fixed", "ecutwfc": 80, "ecutrho": 320}
ELECTRONS = {"conv_thr": 1e-8, "mixing_beta": 0.3}
PSEUDOS = {"Zn": "Zn_ppdojo_SR_NC_PBE.upf", "O": "O_ppdojo_SR_NC_PBE.upf"}
KPTS = (6, 6, 4)


SCF_INPUTNAME = "ZnO.scf.in"
write_espresso_in(
    file=SCF_INPUTNAME,
    atoms=atoms,
    input_data={"control": CONTROL, "system": SYSTEM, "electrons": ELECTRONS},
    pseudopotentials=PSEUDOS,
    kpts=KPTS,
    crystal_coordinates=True,
)
