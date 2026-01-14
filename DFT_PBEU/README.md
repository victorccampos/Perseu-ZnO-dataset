# README

Caracterização eletrônica e estrutural do ZnO via GGA-PBE + U com pseudopotenciais da pseudo-dojo de norma-conservada.

📁  
├── 01_RelaxPBEU  
├── 02_Phonons  
├── 03_Bands  
├── 04_DOS  
└── README.md  





## Otimização da Estrutura


Tiveram algumas estruturas com valores de $E_{gap}$ dentro do range experimental:



|    | fname                   |       a |       c |     c/a |   lowest_unoccupied |   highest_occupied |   Egap | Convergiu   |
|---:|:------------------------|--------:|--------:|--------:|--------------------:|-------------------:|-------:|:------------|
| 12 | ZnO-PBEU-12.00_7.00.out | 3.24806 | 5.19543 | 1.59955 |             10.8287 |             7.4407 | 3.388  | Sim         |
|  8 | ZnO-PBEU-11.50_7.00.out | 3.24771 | 5.19511 | 1.59962 |             10.8334 |             7.4662 | 3.3672 | Sim         |
|  5 | ZnO-PBEU-11.00_7.00.out | 3.24735 | 5.19479 | 1.5997  |             10.8382 |             7.4929 | 3.3453 | Sim         |
|  1 | ZnO-PBEU-10.50_7.00.out | 3.24698 | 5.19446 | 1.59978 |             10.8431 |             7.5209 | 3.3222 | Sim         |
| 14 | ZnO-PBEU-9.50_7.50.out  | 3.24372 | 5.18901 | 1.59971 |             10.9135 |             7.4991 | 3.4144 | Sim         |


Vou verificar como estão as forças nesses arquivos. (**OK**)
    
Vou fabricar um scf com $U_d = 9.50$ e $U_p = 7.50$ e fazer a ***PDOS***; aquele que mais se aproximar da figura do artigo eu escolho.

Tô fazendo assim, pois acho que é melhor se basear *"experimentalmente"* na localização dos estados eletrônicos do que fazer bandas e fônons.