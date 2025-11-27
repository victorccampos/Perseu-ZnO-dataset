# Base de dados Óxido de Zinco para NNPs

Este repositório contém a geração de uma base de dados de estrutura eletrônica e forças atômicas do óxido de zinco (ZnO) utilizando o Quantum ESPRESSO.

O objetivo será de construir uma base de dados de estruturas de ZnO com diferentes geometrias e configurações, obtidas via cálculos ab initio (DFT), com:

- **Energias totais**
- **Forças atômicas**
- **Geometrias distorcidas e/ou próximas ao equilíbrio**

Esses dados serão utilizados para **treinamento e validação de potenciais de campo de força baseados em redes neurais**, como os usados pelo [ænet](https://ann.atomistic.net/), para futuras aplicações em simulações de Dinâmica Molecular.

##  Dependências e Ferramentas

- [Quantum ESPRESSO](https://www.quantum-espresso.org/)
- [ASE (Atomic Simulation Environment)](https://wiki.fysik.dtu.dk/ase/)
- [ænet](https://ann.atomistic.net/)
- Python ≥ 3.8 com bibliotecas:
  - `numpy`, `ase`, `matplotlib`, `pandas`, etc.

	conda create -n qe72_env -c conda-forge qe=7.2 ase numpy pandas matplotlib
---

## Autor

João Victor Campos Costa
Mestrando em Física — Universidade Federal de Minas Gerais
Contato: `victorjvc2020@ufmg.br` | `victorjvc2020@gmail.com`



