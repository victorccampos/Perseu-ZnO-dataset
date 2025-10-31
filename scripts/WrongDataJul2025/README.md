# Disclaimer
Os arquivos de inputs gerados nesse diretório contém uma versão errada do que a missão inicial pretendida  pelo script `get_supercell_dir.py`.

> A ideia era fazer o strain em $\pm$ 10% dos valores obtidos no vc-relax dos parâmetros de rede $a$ e $c/a$.

O que aconteceu na verdade, foi que não se alteraram os parâmetros de rede. Em outras palavras, nos arquivos de input, a seção `CELL_PARAMETERS` se repetiu! A mudança de um arquivo para outro estava apenas em `ATOMIC_POSITIONS`. 

> É possível aproveitar o resultado deste diretório? Se sim como, e com base em qual pensamento físico ??

--- 
# Correção do gerador de inputs do Quantum ESPRESSO.

Uma alteração no arquivo `get_supercell_dir.py` foi feita após a reunião do dia 22 de agosto a partir da inserção do seguinte trecho de código:

```python
 c = a * covera
    new_cell_vectors = [
        [a, 0, 0],
        [-a / 2.0, a * np.sqrt(3) / 2.0, 0],
        [0, 0, c]
    ]

    # 3. Criar uma nova estrutura (Atoms object) com a célula deformada
    # Mantemos os símbolos e as posições fracionais (scaled_positions) do template
    strained_primitive_cell = Atoms(
        symbols = primitive_cell_template.get_chemical_symbols(),
        scaled_positions = primitive_cell_template.get_scaled_positions(),
        cell = new_cell_vectors,
        pbc=True
    )
```
Além disso, escolheu-se (6, 6, 6) como tamanho do __K-Grid__, estipulado em testes de convergência para a célula 1x1x1, elimando a abordagem anterior de "densidade do grid constante" (veja abaixo).

```python
# (Depracated)
# Adapt K-grid to larger supercells, mantaining grid density
    KPOITNS_ORIGINAL = np.array([6, 6, 6])
    KPOINT_SUPERCELL = KPOITNS_ORIGINAL // np.array(cellsize)
    KPOINT_SUPERCELL[KPOINT_SUPERCELL == 0] = 1
```

