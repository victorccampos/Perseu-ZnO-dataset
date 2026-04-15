"""
Class containing post-processing utils for aenet package.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from pathlib import Path


class AenetPP:
    def __init__(
        self, training_set=None, test_set=None, train_out=None, predict_out=None
    ):
        self.training_set: str | Path = training_set
        self.test_set: str | Path = test_set
        self.train_out: str | Path = train_out
        self.predict_out: str | Path = predict_out

    def get_loss(self) -> pd.DataFrame:
        errors = []
        with open(self.train_out) as fp:
            for line in fp:
                if re.match("^ *[0-9].*<$", line):
                    errors.append([float(a) for a in line.split()[1:-1]])

        errors = np.array(errors)
        metrics = ["MAE_train", "RMSE_train", "MAE_test", "RMSE_test"]
        df = pd.DataFrame(data=errors, columns=metrics)
        return df

    def plot_loss(self, save_plot: bool = False) -> None:
        df = self.get_loss()
        epochs = np.arange(1, len(df) + 1)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        title = Path(self.train_out).parent.name
        ax1.set_title(title)
        ax2.set_title(title)

        ax1.plot(epochs, df["RMSE_train"], label="train", color="blue")
        ax1.plot(epochs, df["RMSE_test"], label="test", color="red")

        ax1.set_xlabel("epoch")
        ax1.set_ylabel("E")
        ax1.legend()
        ax1.grid(True, linestyle="--", alpha=0.5)

        # =========================
        # Painel 2: escala log
        # =========================
        ax2.plot(epochs, df["RMSE_train"], label="train")
        ax2.plot(epochs, df["RMSE_test"], label="test")

        ax2.set_xscale("log")
        ax2.set_yscale("log")

        ax2.set_xlabel("epoch")
        ax2.set_title("Log-Scale")
        ax2.legend()
        # ax2.grid(FAL, which='both', linestyle='--', alpha=0.5)

        # --- layout e salvamento ---
        plt.tight_layout()
        if save_plot:
            plt.savefig(
                f"training_{Path(self.train_out).parent.name}.png",
                dpi=300,
                bbox_inches="tight",
            )
        plt.show()
        return

    def summary_loss(self):
        df = self.get_loss()
        has_epoch = "epoch" in df.columns
        metrics = ["RMSE_train", "RMSE_test"]
        summary = {}

        for metric in metrics:
            idx_min = df[metric].idxmin()
            epoch = int(df.loc[idx_min, "epoch"]) if has_epoch else int(idx_min)

            summary[metric] = {
                "min_value": df.loc[idx_min, metric],
                "epoch_at_min": epoch,
            }
        return pd.DataFrame(summary).T

    # Training and test set info
    def get_xsf_energies(self, kind: str) -> pd.DataFrame:
        """
        Lê arquivos .xsf e extrai:
        - nome do arquivo
        - energia total (E_DFT)
        - número de átomos (N_atoms, via linha PRIMCOORD)
        """
        map_kind = {"train": self.training_set, "test": self.test_set}
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
            kind (str): "train" or "test"
        """
        map_kind = {"train": self.training_set, "test": self.test_set}

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
        df["|F|_DFT"] = np.sqrt(df.Fx_DFT**2 + df.Fy_DFT**2 + df.Fz_DFT**2)
        return df

    # Predict
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
        df["|F|_ANN"] = np.sqrt(df.Fx_ANN**2 + df.Fy_ANN**2 + df.Fz_ANN**2)

        return df

    def get_energy_parity(self) -> pd.DataFrame:
        """
        Return a Dataframe comparing energies of DFT vs ANN.
        """

        if not self.predict_out:
            print("predict.out is not defined!")
            return None

        energies_nn = self.get_predict_energies()
        energies_dft = self.get_xsf_energies("test")

        df_parity_energy = pd.concat(
            [energies_dft, energies_nn.drop(columns="filename")], axis=1
        )

        return df_parity_energy

    def get_forces_parity(self) -> pd.DataFrame:
        """Return a DataFrame comparing forces of DFT vs ANN."""

        if not self.predict_out:
            print("predict.out is not defined!")
            return None

        test_forces = self.get_xsf_forces("test")
        predict_forces = self.get_predict_forces()

        forces_df = pd.concat(
            [test_forces, predict_forces.drop("structure", axis=1)], axis=1
        )

        return forces_df
