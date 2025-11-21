import glob
import os
import re
from pprint import pprint

# 1. Define the target range
target_min = 3.3
target_max = 3.44

# 2. Find all files matching the pattern
files = glob.glob("hubbard_scans/zno*.out")

files.sort() # Sort to keep output tidy
match_strucs = []

print(f"{'Filename':<30} | {'Ud':<6} | {'Up':<6} | {'Gap (eV)':<10} | {'Status'}")
print("-" * 80)

for filepath in files:
    filename = os.path.basename(filepath)
    
    # Attempt to extract U values from filename (Assuming format ZnO-LDAU_Ud_Up.out)
    # Adjust the split logic if your naming convention uses dashes instead of underscores
    try:
        # Example: ZnO-LDAU_10.00_7.50.out -> splits by '_'
        parts = filename.replace('.out', '').split('_')
        # print(f'parts of filename = {parts}')
        u_d = parts[1]
        u_p = parts[2]
    except IndexError:
        u_d, u_p = "N/A", "N/A"

    homo = None
    lumo = None
    
    # 3. Read file and find the LAST occurrence
    with open(filepath, 'r') as f:
        for line in f:
            if "highest occupied, lowest unoccupied level (ev):" in line:
                # Standard QE output line looks like:
                # highest occupied, lowest unoccupied level (ev):     7.9083   11.8732
                parts = line.split()
                # print(f'parts of band gap extract = {parts}')
                homo = float(parts[-2])
                lumo = float(parts[-1])
                
    # 4. Calculate and Print
    if homo is not None and lumo is not None:
        gap = lumo - homo
        status = ""
        if target_min <= gap <= target_max:
            status = "<-- MATCH"
            match_strucs.append([filename, gap])
        elif gap > target_max:
            status = "Too High"
        else:
            status = "Too Low"
            
        print(f"{filename:<30} | {u_d:<6} | {u_p:<6} | {gap:.4f}     | {status}")
    else:
        print(f"{filename:<30} | {u_d:<6} | {u_p:<6} | {'Failed':<10} | SCF Not Conv.")

print('*'*100)
pprint(match_strucs)