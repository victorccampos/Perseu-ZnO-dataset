from ase.io import read

structure = read("ZnO-LDAU_12.00_7.00.out")
a, _, c, alpha, beta, gamma = structure.cell.cellpar()

print("Parâmetros de Rede:")
print("{:<5}{:>10.6f}".format("a", a))
print("{:<5}{:>10.6f}".format("c", c))
print("{:<5}{:>10.6f}".format("c/a", c/a))
