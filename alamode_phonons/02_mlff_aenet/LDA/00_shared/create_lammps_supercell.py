from ase import io

if __name__ == "__main__":

   template = "/home/jvc/ZnO_database/DFT_LDA/02_phonon_DFPT/vcrelax.out"
   atoms_primitive = io.read(template)
   supercell = atoms_primitive.repeat((2, 2, 2))
   filename = 'ZnO_supercell.lammps'
   print(f"Writing supercell 2x2x2 to {filename}")
   positions = supercell.get_positions()
   symbols   = supercell.get_chemical_symbols()
   for p, s in zip(positions[:10], symbols[:10]):
       print(p, s)
   species_order = ["Zn", "O"]
   io.write(filename, supercell, format="lammps-data", specorder=species_order)
