import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

def read_dos(filename: str) -> Tuple[np.ndarray, np.ndarray]:
    ener, dos = np.loadtxt(filename, usecols=(0,1), unpack=True)
    return ener, dos

zno_prefix = 'ZnO_950_8'

# Total Density of States
ener, dos = read_dos(f'{zno_prefix}.dos')

# PDOS for Zn d states
ener1, p1_znd = read_dos(f'{zno_prefix}.pdos_atm#1(Zn)_wfc#3(d)') # atm1
ener2, p2_znd = read_dos(f'{zno_prefix}.pdos_atm#2(Zn)_wfc#3(d)') # atm2


EFermi = 4.920 # eV

# Plotting
plt.figure(figsize=(6,5), dpi=600)
plt.plot(ener-EFermi, dos, c='k', label='Total', linewidth=0.5)

# Zn 3d states
plt.plot(ener1-EFermi, p1_znd+p2_znd, c='b', label=r'$Zn_{d}$')
# Preenchimento sob a curva
plt.fill_between(
     ener1 - EFermi,
     p1_znd + p2_znd,
     color='b', alpha=0.2, hatch='xx',

)

# Add the x and y-axis labels
plt.xlabel('Energy (eV)')
plt.ylabel('DOS ')

plt.xlim((-10.5,12))
plt.xticks(range(-10,12,2))
plt.ylim(0, dos.max() + 1)
plt.legend()

plt.savefig(f"{zno_prefix}.pdf", bbox_inches="tight")
plt.savefig(f"{zno_prefix}.png", bbox_inches="tight")
#plt.show()