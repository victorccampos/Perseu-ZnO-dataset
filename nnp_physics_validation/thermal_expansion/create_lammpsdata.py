from ase import io

if __name__ == "__main__":

   template = "/home/jvc/ZnO_database/DFT_LDA/02_phonon_DFPT/vcrelax.out"
   species_order = ["Zn", "O"]
   atoms_primitive = io.read(template)
   shape = (4, 4, 4)
   supercell = atoms_primitive.repeat(shape)

   shape_str = ''.join( map(str, shape) ) # '444' '222'
   filename = f'ZnO-{shape_str}.lammps'

   print(f"Writing supercell {shape_str} to {filename}")
   io.write(filename, supercell, format="lammps-data", specorder=species_order)
