# Relaxação da estrutura  
1. 'vc-relax': permite variar as posições atômicas e constantes de rede.

# Estrutura de bandas.
O cálculo de bandas é non-self consistent field. Dito isso, é executado após o scf pois aproveita deste:  
- ground state electron density $\rho(r)$  
- Hartree  
- exchange and correlation potentials.  

No final do arquivo, dizemos o K-path nos quais queremos calcular os autovalores de energia.  

Exemplo:  
```pw.bands.silicon.out
&control
  calculation = 'bands',
  restart_mode = 'from_scratch',
  prefix = 'silicon',
  outdir = './tmp/'
  pseudo_dir = '../pseudos/'
  verbosity = 'high'
/

.
.
.

K_POINTS {crystal_b}
5
  0.0000 0.5000 0.0000 20  !L
  0.0000 0.0000 0.0000 30  !G
  -0.500 0.0000 -0.500 10  !X
  -0.375 0.2500 -0.375 30  !U
  0.0000 0.0000 0.0000 20  !G
```  

> pw.x < pw.bands.silicon.in > pw.bands.silicon.out  

Após isso executa, o pós-processamento dos dados com pp.bands.silicon.in
&BANDS
  prefix = 'silicon'
  outdir = './tmp/'
  filband = 'si_bands.dat'
/
bands.x < pp.bands.silicon.in > pp.bands.silicon.out
