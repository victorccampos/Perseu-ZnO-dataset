Vou tentar fazer a dispersão de Fônons com as configurações obtidas no arquivo:  

`/home/jvc/QEspresso7.2/ZnO_database/PBE+U_Dataset/RelaxPBE_U/hubbard_scans/outputs/zno_vcrelax_hubbard_11.50_8.00.out`  

O input foi criado com o `qeInputBuilder.py` modificando ao final:

```python
        # Single File
        # Ud = 11.50 e Up = 8.0
        celldm1 =  6.1775348244276 
        celldm1_angstrom = celldm1 * Bohr
        celldm3 = 1.597973765
        ################################
        supercell = transform_primitive_cell((2,2,2), a=celldm1_angstrom, covera=celldm3, primitive_cell_scf='ZnO_template_11.50_8.00.in')               
        make_pwscf_from_atoms(supercell=supercell, create_dir=False)
 ```

 E no arquivo de template pra pegar as posições atômica usei o `ZnO_template_11.50_8.00.in`


    ATOMIC_POSITIONS (crystal)
    Zn               0.6666666667        0.3333333333        0.4990735849
    Zn               0.3333333333        0.6666666667       -0.0009264151
    O                0.6666666667        0.3333333333        0.8812364151
    O                0.3333333333        0.6666666667        0.3812364151