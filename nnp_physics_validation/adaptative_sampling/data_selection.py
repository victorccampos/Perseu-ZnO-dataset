from ase import io, Atoms

import pandas as pd
import numpy as np
from pathlib import Path


import re


def extract_qe_frame_number(filepath: Path) -> int:
    r"""Helper function to properly sort QE files numerically.
    Return the integer value of frame_pwscf_(\d+).out filename.
    """
    match = re.search(pattern=r"frame_pwscf_(\d+)", string=filepath.stem)
    frame_number = int(match.group(1)) if match else -1
    return frame_number


def get_frames(path2data: str | Path, source: str) -> list[Atoms]:
    """
    Args:
        path2data [str]: Path to *.lammpstrj file or directory containing
        outputs "*.out" of Quantum ESPRESSO.
        source [str]: "LAMMPS" | "QE"
    """
    _available_source = ["LAMMPS", "QE"]
    assert_msg = (
        f"Specified source '{source}' is not available in: \n{_available_source}\n"
    )
    assert source in _available_source, assert_msg

    path2data = Path(path2data)

    if source == "LAMMPS":
        # ensure ASE is sorting the atoms by their physical LAMMPS ID
        # ATOMS id type x y z vx vy vz
        # 2 1  1.59809 0.922657 2.56493 1.28797 -0.620794 -0.0514637
        # 3 2  -1.59809e-10 1.84531 1.95076 -0.688782 2.61616 1.76851
        # 4 2  1.59809 0.922657 4.51648 1.45426 3.6468 2.31655
        frames = io.read(
            filename=path2data,
            format="lammps-dump-text",
            index=":",
            specorder=["Zn", "O"],
        )

        # Metadata to LAMMPS Atoms object
        for i, frame in enumerate(frames):
            frame.info["frame_index"] = i

        return frames

    elif source == "QE":
        frames = []

        qe_files = list(path2data.glob("frame_pwscf_*.out"))
        sorted_qe_files = sorted(qe_files, key=extract_qe_frame_number)

        for f in sorted_qe_files:
            atoms = io.read(f, format="espresso-out")
            frame_number = extract_qe_frame_number(f)

            # Metadata to QE Atoms object
            atoms.info["frame_index"] = frame_number
            atoms.info["QE_filepath"] = str(f)

            frames.append(atoms)

        return frames

    return None


def force_dataframe(frames: list[Atoms], source: str):
    """
    Produces a DataFrame of Forces acting on atoms given a list of ASE Atoms
    and the source of the data, e.g, 'QE' or 'LAMMPS'
    """
    _available_source = ["LAMMPS", "QE"]
    assert_msg = (
        f"Specified source '{source}' is not available at: \n{_available_source}\n"
    )

    assert source in _available_source, assert_msg

    data = []

    for frame in frames:
        frame_index = frame.info["frame_index"]
        forces = frame.get_forces()
        symbols: list[str] = frame.get_chemical_symbols()

        for idx_atom, force_vector in enumerate(forces, start=1):
            data.append({
                "frame_index": frame_index,
                "atom_index": idx_atom,
                "atom": symbols[idx_atom - 1],  # 1 based index counting
                f"Fx_{source}": force_vector[0],
                f"Fy_{source}": force_vector[1],
                f"Fz_{source}": force_vector[2],
            })

    df = pd.DataFrame(data)

    return df


def force_parity(
    df_LAMMPS: pd.DataFrame, df_QE: pd.DataFrame, write: bool
) -> pd.DataFrame:
    """
    Merge the force dataframe for Molecular Dynamics (LAMMPS) and DFT (QE)
    snapshots based on columns 'frame-index' and 'atom_index'.
    """
    df_parity = pd.merge(
        left=df_LAMMPS,
        right=df_QE,
        on=["frame_index", "atom_index"],
        how="inner",
        # 'inner' only keep rows where the key combination exists in both DataFrames.
    )
    df_parity = df_parity.drop(columns=["atom_y"])
    df_parity = df_parity.rename(columns={"atom_x": "atom"})
    
    

    
    if write:
        df_parity.to_csv("df_forces_parity.csv", index=False, sep=" ")
    return df_parity

def force_metrics(df_parity: pd.DataFrame, force_error_threshold) -> pd.DataFrame:
    forces_dft = df_parity[["Fx_QE", "Fy_QE", "Fz_QE"]].to_numpy()
    forces_md  = df_parity[["Fx_LAMMPS", "Fy_LAMMPS", "Fz_LAMMPS"]].to_numpy()
    
    # Atom-based -- axis = 1
    deltaF: np.ndarray = forces_dft - forces_md
    df_parity["force_error"] = np.linalg.norm(deltaF, axis=1)  
    
    frame_metrics = (df_parity
                     .groupby(["frame_index"])
                     .agg(
                         max_dF=("force_error", "max"),
                         mean_dF=("force_error", "mean"),
                         dF_rms=("force_error", lambda x: np.sqrt(np.mean(x**2))),
                         std_dF=("force_error", "std"),
                         n_bad_atoms=("force_error", lambda x: (x > force_error_threshold).sum())
                         ).reset_index()
    )
    return frame_metrics


if __name__ == "__main__":
    # Example usage with LAMMPS
    md_trajectory = "../thermal_expansion/100K/trajectories/ZnO-222-100K.lammpstrj"
    md_frames = get_frames(path2data=md_trajectory, source="LAMMPS")
    df_LAMMPS = force_dataframe(md_frames, source="LAMMPS")
    print(df_LAMMPS)
    df_LAMMPS.to_csv("sample_lammps_df.csv", index=False, sep=" ")

    # Example with Quantum-ESPRESSO
    espresso_dir = "./PWSCF-222-100K"
    qe_frames = get_frames(path2data=espresso_dir, source="QE")
    df_QE = force_dataframe(frames=qe_frames, source="QE")
    print(df_QE)
    df_QE.to_csv("sample_qe_df.csv", index=False, sep=" ")

    df_parity = force_parity(df_LAMMPS, df_QE, write=True)
