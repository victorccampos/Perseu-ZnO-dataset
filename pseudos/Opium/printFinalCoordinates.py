file_output = """Begin final coordinates
     new unit-cell volume =    317.50733 a.u.^3 (    47.04973 Ang^3 )
     density =      5.60309 g/cm^3

CELL_PARAMETERS (alat=  6.10000000)
   1.000045315   0.000000000   0.000000000
  -0.500022657   0.866064648   0.000000000
   0.000000000   0.000000000   1.615080812

ATOMIC_POSITIONS (crystal)
Zn               0.6666666667        0.3333333333        0.5006738838
Zn               0.3333333333        0.6666666667        0.0006738838
O                0.6666666667        0.3333333333        0.8796361162
O                0.3333333333        0.6666666667        0.3796361162\n"""
from ase.units import Bohr

# Angstrom
a_angstrom = 6.10000000 * 1.000045315 * Bohr
c_angstrom = 6.10000000 * 1.615080812 * Bohr
razao_ca = c_angstrom / a_angstrom

# Bohr
a = 6.10000000 * 1.000045315
c = 6.10000000 * 1.615080812
razao_ca2 = c / a

print("Output of ZnO_vcrelax.out:\n")
print(file_output)
print("=== Parâmetros de Rede ZnO ===")
print(f"a (Bohr):      {a:.8f}")
print(f"c (Bohr):      {c:.8f}")
print(f"c/a (Bohr):    {razao_ca2:.8f}")
print()
print(f"a (Å):         {a_angstrom:.8f}")
print(f"c (Å):         {c_angstrom:.8f}")
print(f"c/a (Å):       {razao_ca:.8f}")
print("==============================")
