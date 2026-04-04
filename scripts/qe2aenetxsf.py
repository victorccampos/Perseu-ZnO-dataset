"""Convert Quantum ESPRESSO output files into XSF files for AENET.

This script reads SCF `.out` files with ASE's `espresso-out`
reader, extracts the final structure, total energy, and atomic forces, and
formats them as XSF text.

"""

from pathlib import Path

from ase import io
from ase import Atoms


def qe2xsf(scf_out: Path | str) -> str:
    """Return the XSF representation of a Quantum ESPRESSO output file."""
    scf_out = Path(scf_out)
    atoms: Atoms = io.read(scf_out, format="espresso-out")

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

    return "\n".join(xsf)


if __name__ == "__main__":
    data_dir = Path("/home/jvc/ZnO_database/data/LDA_QE_STRUCTURES")
    pwos_pattern = "LDA_*_OUTPUTS/*.out"

    pwos: list[Path] = sorted(data_dir.rglob(pwos_pattern))

    xsf_dir = Path("LDA_xsf_structures")
    xsf_dir.mkdir(exist_ok=True)

    for idx, p in enumerate(pwos, 1):
        try:
            xsf_content = qe2xsf(p)
            fname = xsf_dir / f"LDA-{idx:04d}.xsf"

            with open(fname, "w") as f:
                f.write(xsf_content)

            print(f"[OK] {p} -> {fname}")

        except Exception as e:
            print(f"[FAIL] {p.name}: {e}")
