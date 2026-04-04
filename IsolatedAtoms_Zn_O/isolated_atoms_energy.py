"""
The atomic energies defined in the TYPES section is subtracted from the total
energy before the potential training to reduce the fluctuations in the fitted
energy (the target energy).

Two different approaches towards selecting the atomic energies are shown below:
In Comput. Mater. Sci. 114 (2016) 135-150 the atomic energies are chosen to be
the energies of isolated atoms
"""

from ase.io import read


Zn_atom = read("LDA_Zinc.out", format="espresso-out")
O_atom = read("LDA_Oxygen.out", format="espresso-out")

Zn_energy = Zn_atom.get_total_energy()
O_energy = O_atom.get_total_energy()

print("ISOLATED ENERGY OF ATOMS:\n")
print(f"Zn: {Zn_energy}")
print(f"O: {O_energy}")
