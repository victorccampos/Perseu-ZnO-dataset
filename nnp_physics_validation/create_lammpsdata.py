"""
ASE Script to build supercells of ZnO given a DFT relaxed  structure.
"""
from ase import io
import sys


if __name__ == "__main__":

   pwscf_template = "./vcrelax.out"
   species_order = ["Zn", "O"]
   
   atoms_primitive = io.read(pwscf_template)
   shape = sys.argv[1] if len(sys.argv) > 1 else "222"
   shape = [int(x) for x in shape]
   supercell = atoms_primitive.repeat(shape)

   shape_str = ''.join( map(str, shape) ) # '444' '222'
   filepath = f'./supercells/ZnO-{shape_str}.lammps'

   print(f"Writing supercell {shape_str} to {filepath}")
   io.write(filepath, supercell, format="lammps-data", specorder=species_order)
