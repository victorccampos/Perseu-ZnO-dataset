#!/usr/bin/env python
# coding: utf-8

# In[15]:


from ase.io import read
from ase import Atoms
from ase.build import make_supercell
from ase.units import Bohr

from typing import Tuple


# In[16]:


def transform_unit_cell(supercell_shape: Tuple[int, int, int],
    a: float,
    covera: float,
    template: str = 'ZnO_template.in'
) -> Atoms:
    """
    Transform a primitive cell to a supercell for a given size. 
    """
    primitive_cell: Atoms = read(template, format='espresso-in')
    chemical_symbols: list[str] = primitive_cell.get_chemical_symbols()
    scaled_positions: np.ndarray = primitive_cell.get_scaled_positions()
    
    c = a * covera
    new_cell_vec = np.array([
        [a, 0, 0],
        [-a/2.0, a*(np.sqrt(3)/2.0), 0 ],
        [0, 0, c],
    ])
    
    primitive_cell = Atoms(
        symbols=chemical_symbols, 
        scaled_positions= scaled_positions,
        cell = new_cell_vec,
        pbc=True
    )
    transform_matrix = np.diag(supercell_shape)
    supercell = make_supercell(primitive_cell, transform_matrix)

    # Save supercell dimensions nx, ny, nz in metadata to naming inputs
    supercell.info['shape'] = supercell_shape
    supercell.info['primitive_a'] = a
    supercell.info['primitive_covera'] = covera

    return supercell


# In[17]:


prim_cell_path: str = "./ZnO_scf_primcell.in"

