"""
Post-processing helper for analyzing outputs from ænet-PyTorch training and
prediction runs on ZnO datasets.

The file defines a single class, `AenetPy`, which reads:

- `train.error`, produced during ænet-PyTorch training.
- `predict.out`, produced during ænet prediction.
- `.xsf` structure files containing DFT total energies and atomic forces.

It returns `pandas.DataFrame` objects for downstream analysis and provides
helpers for plotting loss curves and computing force RMSE values.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from pathlib import Path


class AenetPy:
    def __init__(
        self, training_set=None, validation_set=None, train_out=None, predict_out=None
    ):
        """
        training_set: path do directory containg XSF files
        validation_set: path do directory containg the independent XSF files
        train_out: path to "train.error" file
        predict_out: path to "predict.out" file
        """
        self.training_set: str | Path | None = training_set
        self.validation_set: str | Path | None = validation_set
        self.train_out: str | Path | None = train_out
        self.predict_out: str | Path | None = predict_out

    def get_loss(self) -> pd.DataFrame:
        """Lê o train.error do ænet-PyTorch e retorna DataFrame da tabela de treinamento."""
        errors = np.loadtxt(self.train_out)
        columns = [
            "epoch",
            "ERROR_train",
            "ERROR_test",
            "E_train",
            "E_test",
            "F_train",
            "F_test",
        ]
        return pd.DataFrame(data=errors, columns=columns)

    def plot_loss(self):

        df: pd.DataFrame = self.get_loss()

        fig, axes = plt.subplots(
            nrows=3, ncols=2, figsize=(12, 10), layout="constrained"
        )
        fig.suptitle("Training Curves - ænet PyTorch", size=20)

        plots = [
            (["ERROR_train", "ERROR_test"], "Total Error"),
            (["E_train", "E_test"], "Energy Error"),
            (["F_train", "F_test"], "Force Error"),
        ]
        colors = ["blue", "red"]
        # Iteração sobre as linhas (i) e os dados do gráfico
        for i, (cols, title) in enumerate(plots):
            df[cols].plot(ax=axes[i, 0], title=title, grid=True, color=colors)
            df[cols].plot(
                ax=axes[i, 1],
                title=f"{title} (Log)",
                logy=True,
                logx=True,
                grid=True,
                color=colors,
            )

        plt.show()

    def summary_loss(self):

        df = self.get_loss()

        metrics = [col for col in df.columns if col != "epoch"]

        summary = {}

        for metric in metrics:
            idx_min = df[metric].idxmin()
            summary[metric] = {
                "min_value": df.loc[idx_min, metric],
                "epoch_at_min": int(df.loc[idx_min, "epoch"]),
            }

        return pd.DataFrame(summary).T

    def get_xsf_energies(self, kind: str) -> pd.DataFrame:
        """
        Lê arquivos .xsf e extrai:
        - nome do arquivo
        - energia total (E_DFT)
        - número de átomos (N_atoms, via linha PRIMCOORD)
        """
        map_kind = {"train": self.training_set, "test": self.validation_set}
        filepath = Path(map_kind[kind])
        pattern_energy = re.compile(r"#\s*total energy\s*=\s*([-+]?\d*\.\d+|\d+)\s*eV")
        pattern_natoms = re.compile(r"PRIMCOORD\s*\n\s*(\d+)\s+\d+")

        data = []
        for file in sorted(filepath.glob("*.xsf")):
            text = file.read_text()

            match_e = pattern_energy.search(text)
            match_n = pattern_natoms.search(text)

            if match_e and match_n:
                energy = float(match_e.group(1))
                natoms = int(match_n.group(1))
                data.append((file.name, energy / natoms))

        return pd.DataFrame(data, columns=["filename", "E_DFT (eV/atom)"])

    def get_xsf_forces(self, kind: str) -> pd.DataFrame:
        """
        Retorna as forças contidas em um conjunto de XSF
            kind (str): "train" or "validation"
        """
        map_kind = {"train": self.training_set, "validation": self.validation_set}

        filepath = Path(map_kind[kind])
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

    def get_predict_energies(self) -> pd.DataFrame:
        text = Path(self.predict_out).read_text()

        # Captura: nome do arquivo .xsf, energia total
        pattern = (
            r"File name\s*:\s*(\S+\.xsf).*?"
            r"Number of atoms\s*:\s*(\d+).*?"
            r"Total energy\s*:\s*([-\d.]+).*?"
            # r"RMS force\s*:\s*([-\d.]+)"
        )

        matches = re.findall(pattern, text, re.S)

        df = pd.DataFrame(matches, columns=["filename", "n_atoms", "E_ANN (eV)"])

        df["filename"] = df["filename"].apply(lambda x: Path(x).name)
        df["E_ANN (eV)"] = df["E_ANN (eV)"].astype(float)
        df["n_atoms"] = df["n_atoms"].astype(int)
        df["E_ANN (eV/atom)"] = df["E_ANN (eV)"] / df["n_atoms"]

        return df[["filename", "E_ANN (eV/atom)"]]

    def get_predict_forces(self) -> pd.DataFrame:
        """Lê predict.out do ænet e retorna DataFrame com nome da estrutura e forças (Fx, Fy, Fz)."""
        if not self.predict_out:
            print("predict.out is not defined!")
            return None

        data = []
        with open(self.predict_out, "r") as f:
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

    def get_forces_df(self) -> pd.DataFrame:
        """
        Creates a DataFrame to compare Forces DFT vs ANN.
        """
        if not self.predict_out:
            print("predict.out is not defined!")
            return None

        dft_forces = self.get_xsf_forces(kind="test")
        predict_forces = self.get_predict_forces()

        df_forces = pd.concat(
            [dft_forces, predict_forces.drop("structure", axis=1)], axis=1
        )
        df_forces["|F|_DFT"] = np.sqrt(
            df_forces.Fx_DFT**2 + df_forces.Fy_DFT**2 + df_forces.Fz_DFT**2
        )
        df_forces["|F|_ANN"] = np.sqrt(
            df_forces.Fx_ANN**2 + df_forces.Fy_ANN**2 + df_forces.Fz_ANN**2
        )
        return df_forces

    def get_RMSE_forces(self) -> np.ndarray:
        """Numpy Array with RMSE: (Fx,Fy,Fz) in eV/Angstrons"""

        if not self.predict_out:
            print("predict.out is not defined!")
            return None

        df_forces = self.get_forces_df()
        RMSE_Fx = np.sqrt(np.mean((df_forces.Fx_ANN - df_forces.Fx_DFT) ** 2))
        RMSE_Fy = np.sqrt(np.mean((df_forces.Fy_ANN - df_forces.Fy_DFT) ** 2))
        RMSE_Fz = np.sqrt(np.mean((df_forces.Fz_ANN - df_forces.Fz_DFT) ** 2))
        # RMSE in eV/Ang
        return np.array([RMSE_Fx, RMSE_Fy, RMSE_Fz])
