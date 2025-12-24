"""
This script analyzes and plots the convergence of total energy per atom with respect to the kinetic energy cutoff (ecut) in Quantum ESPRESSO self-consistent field (SCF) calculations.

Main functionalities:
- Reads multiple SCF output files and extracts the total energy per atom.
- Organizes the extracted data into a pandas DataFrame, computing energy differences relative to the minimum energy and between consecutive cutoffs.
- Plots the energy per atom and the energy differences as a function of the kinetic energy cutoff, highlighting convergence thresholds and optionally saving the figure.

Functions:
- get_energies(scf_outputs): Reads SCF output files from a directory and returns a list of filenames and corresponding energies per atom.
- transform_data_to_df(data): Converts the list of energies into a DataFrame and computes energy differences for convergence analysis.
- plot_convergence(df, pseudopot_title, save): Plots the energy convergence data, with options for customization and saving the figure.

Usage:
- Configure the SCF output directory and pseudopotential information in the main block.
- Run the script to generate and display/save convergence plots for the specified pseudopotential.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from ase.io import read
from pathlib import Path


def get_deltaE_consec(x):
    """Returns [0, E_{i+1} - E_{i}]"""
    return np.abs(np.r_[0, np.diff(x)])  # r_ concatena


def get_deltaEref(x):
    """Returns |E_i - E_ref|, where E_ref = min(E)"""
    return np.abs(x - np.min(x))


def get_energies(kpoint_outfiles: str) -> list[list[str, float]]:
    """
    Lê todos os arquivos kpoint.*.out, extrai a energia por átomo em eV.

    Output: [['kpoint*.out', E/atom (eV)], ...]
    """
    NUM_ATOMOS = 4

    files = list(Path(kpoint_outfiles).glob("kpoint*.out"))
    energies = [
        read(f, format="espresso-out").get_total_energy() / NUM_ATOMOS for f in files
    ]

    data: list[list[str, float]] = [[f.name, e] for f, e in zip(files, energies)]
    # Ordem descrescente de energia.
    data.sort(key=lambda x: x[1], reverse=True)
    return data


def transform_data_to_df(data: list) -> pd.DataFrame:
    """
    Cria um DataFrame com informação das energias.
    File	E/atom	dE_ref_meV	dE_consec_meV.

    dE_ref_meV: E_min - E_i
    dE_consec_meV : E_{i+1} - E_{i}
    """

    df = pd.DataFrame(data, columns=["File", "E/atom"])
    df["dE_ref_meV"] = get_deltaEref(df["E/atom"]) * 1_000
    df["dE_consec_meV"] = get_deltaE_consec(df["E/atom"]) * 1_000

    return df


def plot_kgrid_convergence(df: pd.DataFrame, pdf_name: str, figure_title: str):
    """
    Args:
        data: DataFrame with columns: File	E/atom	dE_ref_meV	dE_consec_meV
        pdf_name: name of the output figure file (pdf).
        figure_title: string containing info about selected pseudopotential.
    """
    THR = 2.0  # meV
    YMAX = 10.0  # Limite superior para clipar os valores no gráfico de diferenças.

    kpoints = np.arange(4, 15)

    E_per_atom = df["E/atom"].to_numpy()
    dE_ref_meV = df["dE_ref_meV"].to_numpy()
    dE_consec_meV = df["dE_consec_meV"].to_numpy()

    fig, (axE, axdE) = plt.subplots(
        2,
        1,
        sharex=True,
        figsize=(6, 6),
        dpi=300,
        gridspec_kw={"hspace": 0.05},
        layout="constrained",
    )

    # === Painel (a): energia por átomo vs kgrid ===
    axE.set_title(figure_title)
    axE.set_ylabel(r"$E$ (eV/atom)")
    axE.plot(kpoints, E_per_atom, marker="s", ls="-", color="black", label=r"$E_i$")
    axE.scatter(kpoints[-1], E_per_atom[-1], marker="v", color="black")
    axE.legend()

    # === Painel (b): diferenças em meV/átomo ===

    dE_ref_abs = np.abs(dE_ref_meV)
    dE_consec_abs = np.abs(dE_consec_meV)

    # Versões "clipadas"
    dE_ref_plot = np.clip(dE_ref_abs, 0, YMAX)
    dE_consec_plot = np.clip(dE_consec_abs, 0, YMAX)

    axdE.plot(
        kpoints, dE_ref_plot, marker="s", ls="-", label=r"$|E_i - E_{\mathrm{ref}}|$"
    )
    axdE.plot(kpoints, dE_consec_plot, marker="o", ls="--", label=r"$|E_i - E_{i-1}|$")

    # Faixa de tolerância 0–2 meV/átomo
    axdE.axhspan(0.0, THR, alpha=0.15, color="red")

    axdE.set_ylabel(r"$\Delta E$ (meV/atom)")
    axdE.set_xlabel(r"k-grid", labelpad=10)
    axdE.set_ylim(0, YMAX)

    axdE.legend()

    fig.savefig(pdf_name, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    plt.style.use("/home/jvc/ZnO_database/mpl_themes/jvc.mplstyle")

    # Pseudo-Dojo
    kpoint_outfiles = "/home/jvc/ZnO_database/pseudos/ppdojo_LDA/kpoints"
    data = get_energies(kpoint_outfiles)
    df = transform_data_to_df(data)

    plot_kgrid_convergence(
        df,
        pdf_name="ppdojo_kgrid_convergence_LDA.pdf",
        figure_title="Pseudo-Dojo LDA NC",
    )
