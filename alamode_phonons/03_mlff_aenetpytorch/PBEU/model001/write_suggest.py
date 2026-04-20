"""
Write a alm_suggest.in for Zinc Oxide
based on a Atoms Object
"""

from ase.io import read
import ase.units as units

primitive = read("ZnO-PBEU-9.50_7.50.out")
supercell = primitive.repeat((2, 2, 2))
hexagonal_base_vectors = primitive.cell / primitive.cell[0][0]
prefix = "pbeu_mlff"
spec_order = ["Zn", "O"]

suggest_string = f"""&general
PREFIX = {prefix}
MODE = suggest
NAT = {len(supercell)}
NKD = {len(set(supercell.get_chemical_symbols()))}
KD =  {" ".join(spec_order)}
/

&interaction
NORDER = 1
/

&cell
{supercell.cell[0][0] / units.Bohr}
{" ".join([str(ai) for ai in hexagonal_base_vectors[0]])}
{" ".join([str(bi) for bi in hexagonal_base_vectors[1]])}
{" ".join([str(ci) for ci in hexagonal_base_vectors[2]])}
/

&cutoff 
  Zn-Zn None
  O-O None
  Zn-O None
/

&position 
"""

symbols = ["1" if sym == "Zn" else "2" for sym in supercell.get_chemical_symbols()]
scaled_positions = supercell.get_scaled_positions()

for symbol_num, pos in zip(symbols, scaled_positions):
    suggest_string += f"{symbol_num} {' '.join(str(x) for x in pos)}\n"


with open("01_pbeu_suggest.in", "w") as fp:
    fp.write(suggest_string)
