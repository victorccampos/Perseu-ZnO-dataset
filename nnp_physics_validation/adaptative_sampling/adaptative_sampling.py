"""Convert Quantum ESPRESSO output files into XSF files for AENET.

This script reads SCF `.out` files with ASE's `espresso-out`
reader, extracts the final structure, total energy, and atomic forces, and
formats them as XSF text.

"""

from ase import io, Atoms
from pathlib import Path


def qe2aenetxsf(pwscf_output: Path | str, xsf_name: str) -> str:
    """Return the XSF representation of a Quantum ESPRESSO output file."""
    pwscf_output = Path(pwscf_output)
    atoms: Atoms = io.read(pwscf_output, format="espresso-out")

    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()

    xsf = [f"# total energy = {energy} eV", ""]

    if atoms.pbc.any():
        xsf += ["CRYSTAL", "PRIMVEC"]
        for v in atoms.get_cell():
            xsf.append(f"{v[0]} {v[1]} {v[2]}")
        xsf += ["PRIMCOORD", f"{len(atoms)} 1"]
    else:
        xsf += ["ATOMS"]

    atom_line = (
        "{atom.symbol:<3s} "
        "{atom.x: .12f} {atom.y: .12f} {atom.z: .12f} "
        "{f[0]: .12f} {f[1]: .12f} {f[2]: .12f}"
    )

    xsf += [atom_line.format(atom=atom, f=forces[i]) for i, atom in enumerate(atoms)]
    content = "\n".join(xsf)

    with open(xsf_name, "w") as f:
        f.write(content)
    return content


def write_xsf_output_frames(espresso_dir: str | Path) -> None:
    """Write the ænet-XSF files of Quantum ESPRESSO outputs from a given directory"""
    
    espresso_dir = Path(espresso_dir)
    espresso_outputs = [f for f in espresso_dir.iterdir() if f.suffix == ".out"]
    
    for file in espresso_outputs:
        qe2aenetxsf(pwscf_output=file, xsf_name=file.with_suffix(".xsf"))

    return None
        
