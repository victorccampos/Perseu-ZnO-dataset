from ase.io import read


zno_lda = read("/home/jvc/ZnO_database/DFT_LDA/02_phonon_DFPT/ZnO.scf.in")
zno_pbeu = read("/home/jvc/ZnO_database/DFT_PBEU/02_Phonons/ZnO.scf.in")

print("LDA")
print(zno_lda.cell.array)
print()
print("PBE + U")
print(zno_pbeu.cell.array)
zno_lda.write("zno_lda.xsf")
zno_lda.write("zno_pbeu.xsf")
