from ase.units import Ry
from ase.io import read



Zn_atom = read('Zinc.out', format='espresso-out')
O_atom = read('Oxygen.out', format='espresso-out')



print(f'O atom energy', O_atom.get_total_energy())
print(f'Zinc atom energy', Zn_atom.get_total_energy())