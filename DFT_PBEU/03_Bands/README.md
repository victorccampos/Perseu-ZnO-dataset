# README

> Este diretório contém a estrutura de bandas com GGA+U.


Tiveram alguns registros que couberam no range experimental:



|    | fname                   |       a |       c |     c/a |   lowest_unoccupied |   highest_occupied |   Egap | Convergiu   |
|---:|:------------------------|--------:|--------:|--------:|--------------------:|-------------------:|-------:|:------------|
| 12 | ZnO-PBEU-12.00_7.00.out | 3.24806 | 5.19543 | 1.59955 |             10.8287 |             7.4407 | 3.388  | Sim         |
|  8 | ZnO-PBEU-11.50_7.00.out | 3.24771 | 5.19511 | 1.59962 |             10.8334 |             7.4662 | 3.3672 | Sim         |
|  5 | ZnO-PBEU-11.00_7.00.out | 3.24735 | 5.19479 | 1.5997  |             10.8382 |             7.4929 | 3.3453 | Sim         |
|  1 | ZnO-PBEU-10.50_7.00.out | 3.24698 | 5.19446 | 1.59978 |             10.8431 |             7.5209 | 3.3222 | Sim         |
| 14 | ZnO-PBEU-9.50_7.50.out  | 3.24372 | 5.18901 | 1.59971 |             10.9135 |             7.4991 | 3.4144 | Sim         |


Vou verificar como estão as forças nesses arquivos. (**OK**)
    
Vou fabricar um scf com $U_d = 9.50$ e $U_p = 7.50$ e fazer a ***PDOS***; aquele que mais se aproximar da figura do artigo eu escolho. Acho que é melhor se basear *"experimentalmente"* na localização dos estados eletrônicos do que fazer bandas e fônons.

---

**Dielectric properties and Raman spectra of ZnO from a first principles finite-differences/finite-fields approach**

![](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fsrep02999/MediaObjects/41598_2013_Article_BFsrep02999_Fig3_HTML.jpg?)

