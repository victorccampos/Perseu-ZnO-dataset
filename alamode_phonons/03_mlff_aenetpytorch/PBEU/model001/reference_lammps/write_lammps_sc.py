"""
Create a lammps-data file given a template of
primitive cell obtained via ab-inito calculations.

Note: You must take care the order of the atoms,
controlled by the argument `specorder`.
"""

from ase import io

if __name__ == "__main__":
    # primitive = io.read("ZnO-PBEU-9.50_7.50.out")
    primitive = io.read(
        "/home/jvc/ZnO_database/data/PBEU_QE_STRUCTURES/PBEU_000_INPUTS/ZnO-3.24-1.60-222.in"
    )
    # supercell = primitive.repeat((2, 2, 2))
    supercell = primitive.copy()

    print("Atomic Positions in Angstroms:\n")
    positions = supercell.get_positions()
    symbols = supercell.get_chemical_symbols()
    for p, s in zip(positions[:10], symbols[:10]):
        print(s, *p)

    FILENAME = "pbeu_supercell.lammps"
    print(f"Writing supercell 2x2x2 to {FILENAME}")
    species_order = ["Zn", "O"]
    io.write(
        FILENAME,
        supercell,
        format="lammps-data",
        specorder=species_order,
    )

    # Verify structure using Matterviz extension
    atoms_lammps = io.read(FILENAME, format="lammps-data", Z_of_type={1: 30, 2: 8})
    atoms_lammps.write("pbeu_supercell.cif")
