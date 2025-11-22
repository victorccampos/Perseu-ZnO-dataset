1. vc-relax
Extrair o bloco das constantes de rede e pos. atômicas:
grep -Pzo '(?s)Begin final coordinates.*?End final coordinates' arquivo.out

2. Rodar o scf com constantes otimizadas do passo 1 e produzir o xsf.
