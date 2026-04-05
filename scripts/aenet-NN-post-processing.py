import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from pathlib import Path


def get_training_table(file: str) -> pd.DataFrame:
    """Lê o train.out e extrai a tabela de treinamento."""
    errors = []
    with open(file) as fp:
        for line in fp:
            if re.match("^ *[0-9].*<$", line):
                errors.append([float(a) for a in line.split()[1:-1]])

    errors = np.array(errors)
    df = pd.DataFrame(
        data=errors, columns=["MAE_train", "RMSE_train", "MAE_test", "RMSE_test"]
    )
    return df


def get_dft_energies(xsfs_dir: str) -> pd.DataFrame:
    """
    Lê arquivos .xsf e extrai:
      - nome do arquivo
      - energia total (E_DFT)
      - número de átomos (N_atoms, via linha PRIMCOORD)
    """
    pattern_energy = re.compile(r"#\s*total energy\s*=\s*([-+]?\d*\.\d+|\d+)\s*eV")
    pattern_natoms = re.compile(r"PRIMCOORD\s*\n\s*(\d+)\s+\d+")

    data = []
    for file in sorted(Path(xsfs_dir).glob("*.xsf")):
        text = file.read_text()

        match_e = pattern_energy.search(text)
        match_n = pattern_natoms.search(text)

        if match_e and match_n:
            energy = float(match_e.group(1))
            natoms = int(match_n.group(1))
            data.append((file.name, energy, natoms))

    return pd.DataFrame(data, columns=["filename", "E_DFT (eV)", "N_atoms"])


def get_predict_energies(predict_out: str) -> pd.DataFrame:
    """
    Lê o arquivo predict.out do ænet e extrai:
      - nome do arquivo XSF
      - energia total (eV)
    Retorna um DataFrame com colunas:
      ['filename', 'total_energy_ann (eV)']
    """
    text = Path(predict_out).read_text()

    # Captura: nome do arquivo .xsf, energia total
    pattern = (
        r"File name\s*:\s*(\S+\.xsf).*?"
        r"Total energy\s*:\s*([-\d.]+).*?"
        # r"RMS force\s*:\s*([-\d.]+)"
    )

    matches = re.findall(pattern, text, re.S)

    df = pd.DataFrame(matches, columns=["filename", "E_ANN (eV)"])
    df["E_ANN (eV)"] = df["E_ANN (eV)"].astype(float)
    # df['rms_force (eV/Å)'] = df['rms_force (eV/Å)'].astype(float)

    # Remove caminhos e deixa só o nome do arquivo (ex: structure0003.xsf)
    df["filename"] = df["filename"].apply(lambda x: Path(x).name)

    return df


def read_predict_forces(filepath: str) -> pd.DataFrame:
    """Lê predict.out do ænet e retorna DataFrame com nome da estrutura e forças (Fx, Fy, Fz)."""
    data = []
    with open(filepath, "r") as f:
        lines = f.readlines()

    structure = None
    for line in lines:
        if line.strip().startswith("File name"):
            structure = line.split(":")[1].strip()
            structure = structure.split("/")[-1:][0]
        elif re.match(r"^\s*(Zn|O)\s", line):
            parts = line.split()
            atom, x, y, z, fx, fy, fz = parts
            data.append([structure, float(fx), float(fy), float(fz)])

    df = pd.DataFrame(data, columns=["structure", "Fx_ANN", "Fy_ANN", "Fz_ANN"])
    return df


def read_xsf_forces(xsf_dir: Path) -> pd.DataFrame:
    filepath = Path(xsf_dir)
    data = []
    for xsf_file in sorted(filepath.iterdir()):
        filename = xsf_file.name
        with open(xsf_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            if re.match(r"^\s*(Zn|O)\s", line):
                parts = line.split()
                atom, x, y, z, fx, fy, fz = parts
                data.append([filename, float(fx), float(fy), float(fz)])
    df = pd.DataFrame(data, columns=["structure", "Fx_DFT", "Fy_DFT", "Fz_DFT"])
    return df
