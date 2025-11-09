from pathlib import Path
import pandas as pd
import pprint
from ase.io import read
from ase.units import Bohr

files: list[Path] = list(Path('hubbard_scans').glob('zno_vcrelax_hubbard_*.out'))

data_gaps = {}

for file in files:
    text: list[str] = file.read_text().split('\n')
    for idx, line in enumerate(text):
        
        # Band Gap
        if line.startswith('     highest occupied'):
            highest, lowest = line.split(':')[-1:][0].strip().split()
            band_gap = float(lowest) - float(highest)
            # ZnO Band Gap ~ 3.37
            band_gap = round(band_gap, 2) 
            # print(f'{highest} {lowest} -> band gap: {float(lowest) - float(highest)}')
            data_gaps[file] = band_gap
        

data_gaps = dict(sorted(data_gaps.items(), key=lambda item: item[1], reverse=True))

good_band_gaps = {k:v for k,v in data_gaps.items() if v > 3.2 and v < 3.4}



print('\n{:>35} | {:^10} | {:^10} | {:^10} | {:^10} |'.format('File', 'a (Å)', 'c (Å)', 'c/a', 'Egap (eV)'))
print('-' * 90)

for file, Egap in good_band_gaps.items():
    atoms = read(file)
    a, b, c = atoms.cell.lengths()
    print('{:>35} | {:10.4f} | {:10.4f} | {:10.4f} | {:10.2f} |'.format(
        file.name, a, c, c/a, Egap))

    if Egap == 3.37:
        print(f'\nBest Result for energy band gap: {file.name}:')
        print(f'\tAtomic Positons:')
        print(f'{atoms.get_scaled_positions()}\n')
    else:
        continue