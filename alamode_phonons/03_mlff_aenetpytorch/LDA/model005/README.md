
```
TRAININGSET /home/victorcampos/aenet-PyTorch/DatasetLDA/models/model005/ZnO_LDA.train.ascii
TESTPERCENT 20
ITERATIONS 2000
ITERWRITE 1
BATCHSIZE 256

!SAVE_ENERGIES
!SAVE_FORCES

VERBOSE

MEMORY_MODE gpu

FORCES
alpha=0.2

METHOD
method=adamw lr=0.0001

REGULARIZATION 1e-05

NETWORKS
! atom        network_file     hidden_layers       nodes:activation
! types  
Zn            Zn.pytorch.nn     3            25:tanh 25:tanh 25:tanh 
O             O.pytorch.nn      3            25:tanh 25:tanh 25:tanh   
```
