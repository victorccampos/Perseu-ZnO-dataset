import sys
import re
import pprint

# Output file from self-consistent field calculation
output_file: str = sys.argv[1]

with open(output_file, 'r') as f:
    data: str = f.read()

### Extract total energy (Ry)
total_energy_pattern_in_QE = r"!\s+total energy\s+=\s+([-\d.]+)\s+Ry"
energy_match = re.search(
    pattern = total_energy_pattern_in_QE,
    string = data
    )
total_energy = float(energy_match.group(1)) if energy_match else 0.0

######################## Extract forces in (Ry/au)##############################
##############################
                                    # Forces acting on atoms (cartesian axes, Ry/au):
# atom    1 type  1   force =       # non-local contrib.
# atom    2 type  1   force =       # ionic contribution
# atom    3 type  2   force =       # local contribution
# atom    4 type  2   force =       # core correction contribution
                                    # Hubbard contrib.                                    
                                    # SCF correction ter
################################################################################
forces = []
forces_pattern_in_QE = r"atom\s+\d+\s+type\s+\d+\s+force\s+=\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)"

force_matches = re.finditer(forces_pattern_in_QE, data)


# Stores Fx, Fy, Fz
atomic_species = []

i_trunc = 4

for index, match in enumerate(force_matches):
    # Pegar apenas 4 primeiras linhas dos dados de Força
    if index < i_trunc:
        # print(f'index = {index}')
        atomic_species.append(match.group().split()[:4])
        # print(rf'{match.group()= }')
        
        forces.append([
            float(match.group(1)), # Fx
            float(match.group(2)), # Fy
            float(match.group(3))  # Fz
            ])
    


    

pprint.pprint(atomic_species)
pprint.pprint(forces) 
# print(len(forces))   
# pprint.pprint(force_output)
################################################################################