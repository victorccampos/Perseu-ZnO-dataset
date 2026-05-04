# ZnO Database - Data Directory

## Descrição

Este diretório contém dados relacionados ao banco de dados de óxido de zinco (ZnO).


## Estrutura do Diretório

```sh
data/  
├── datasets/          # Conjuntos de dados em XSF      (git ignored)  
├── raw/               # Dados brutos (PWSCF IO)        (git ignored)  
├── subsets/           # Dados processados              (git ignored)    
├── raw_LDA_QE.tar.gz  # PWSCF LDA -- compressed
├── raw_PBEU_QE.tar.gz  # PWSCF LDA -- compressed
├── README.md  

```

## Conteúdo

- **raw**: Dados brutos antes de qualquer transformação
- **datasets**: Contém os XSF (formato aenet) do ZnO.
- **subsets**: Dados que foram pré-processados e preparados para análise    