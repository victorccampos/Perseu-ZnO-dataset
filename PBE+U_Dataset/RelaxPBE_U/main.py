from pathlib import Path
import pandas as pd
from pprint import pprint
from ase.io import read
from ase.units import Bohr

files: list[Path] = list(
    Path('hubbard_scans').glob('zno_vcrelax_hubbard_*.out')
    )

print(f'Total number of files = {len(files)}')
idxs_to_drop: list[int] = []
for idx, file in enumerate(files):
    with open(file, 'r') as f:
        data = f.readlines()
        for line in data:
            if 'Error in routine bfgs (1)' in line:
                idxs_to_drop.append(idx)

print(f'Total BFGS Errors {len(idxs_to_drop)}')
converged_files = [file for i, file in enumerate(files) if i not in idxs_to_drop]
print(f'Converged Files: {len(converged_files)}\n')    

# ======================= Extract Physical Data ============================== #

data_gaps: dict[Path, float] = {}
extract_gap_from_line = lambda x : x.split(':')[-1:][0].strip().split()

for file in converged_files:
    text = file.read_text().split('\n') 
    for line in text:
        if ('     highest occupied') in line:
            highest, lowest = extract_gap_from_line(line)
            band_gap = float(lowest) - float(highest)
            if band_gap > 3.2 and band_gap < 3.4: 
                #print(file.name, round(band_gap, 3))
                data_gaps[file] = round(band_gap,3)


data_gaps = dict(
    sorted(data_gaps.items(), key= lambda item: item[1]) # sort by Egap
)

def get_lattice_params(file: Path, gap_dict: dict):
    atoms = read(file, format='espresso-out')
    a, b, c = atoms.cell.lengths()
    ratio_ca = c/a
    egap = gap_dict[file]

    return {file.name:  [a, c, ratio_ca, egap] }

phys_info = [get_lattice_params(f, data_gaps) for f in data_gaps.keys()]

columns = ['File', 'a (Å)', 'c (Å)', 'c/a Ratio', 'Band Gap (eV)']

phys_info_df = pd.DataFrame(
    [ [file, *values] for info in phys_info for file, values in info.items()],
    columns=columns
)


# phys_info_df.to_csv('vcrelax_physical_info.csv', index=False)
pprint(phys_info_df)

