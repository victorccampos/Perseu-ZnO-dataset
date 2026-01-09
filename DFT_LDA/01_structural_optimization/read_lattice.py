from ase.io import read

structure = read("vcrelax.out")
a, _, c, alpha, beta, gamma = structure.cell.cellpar()

print("Parâmetros de Rede:")
print("{:<5}{:>10.6f}".format("a", a))
print("{:<5}{:>10.6f}".format("c", c))
print("{:<5}{:>10.6f}".format("c/a", c/a))
