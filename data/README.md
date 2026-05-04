# ZnO Database - Data Directory

## Descrição

Este diretório contém dados relacionados ao banco de dados de óxido de zinco (ZnO).


## Estrutura do Diretório

```sh
.
├── dataset   # XSF's
│   ├── LDA_dataset  
│   └── PBEU_dataset  
├── dataset_LDA.tar.xz  
├── dataset_PBEU.tar.xz  
├── LDA_normal_modes.tar.xz  
├── raw    # I/O do PWSCF 
│   ├── LDA_QE  
│   └── PBEU_QE  
├── raw_LDA_QE.tar.gz  
├── raw_PBEU_QE.tar.xz  
├── README.md # Este arquivo  
└── subsets  
    ├── 01_LDA_dataset_clean   # Subset de LDA_dataset com filtros (Notebooks/LDA_dataset_analysis.ipynb)
    ├── normal_modes_LDA       # Normal mode sampling  
    └── README.md  

```

## Conteúdo

- **raw**: Dados brutos antes de qualquer transformação
- **datasets**: Contém os XSF (formato aenet) do ZnO.
- **subsets**: Dados que foram pré-processados e preparados para análise    