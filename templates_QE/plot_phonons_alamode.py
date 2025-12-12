"""
Python script to plot phonon dispersion obtained via ALAMODE calculation.
The Experimental Data are extracted from: DOI 10.1038/srep22504
Thermal Conductivity of Wurtzite Zinc-Oxide from First-Principles Lattice Dynamics
- A Comparative Study with Gallium Nitride
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import pandas as pd


def get_alamode_data(alamode_bands: str):
    """
    Return: k-axis and eigenvalues in cm^-1
    """
    data = np.loadtxt(alamode_bands, skiprows=3)
    return data


def get_brillouin_info(alamode_bands: str):
    """Info about high symmetry path to be plotted"""
    with open(alamode_bands) as f:
        high_symmetry_labels: str = f.readline().strip()
        high_symmetry_points: str = f.readline().strip()

    xticks: list[float] = [float(x) for x in high_symmetry_points.lstrip("#").split()]
    labels: list[str] = high_symmetry_labels.lstrip("#").split()

    xtick_labels = []
    for lab in labels:
        if lab == "G":
            xtick_labels.append(r"$\Gamma$")
        else:
            xtick_labels.append(f"{lab}")

    return xticks, xtick_labels


if __name__ == "__main__":
    # ALAMODE data
    alamode_bands = "ZnO222_NA3.bands"
    data: np.ndarray = get_alamode_data(alamode_bands)

    q_axis = data[:, 0]
    freqs_invcm = data[:, 1:]

    # Conversão unidades
    invcm_to_thz = 1.0 / 33.35641
    freqs_thz = freqs_invcm * invcm_to_thz

    # Experimental
    EXPDATA_DIR = "./ExpDataRefs"
    path_to_exp = [
        f"{EXPDATA_DIR}/ZnO_Phonons_Ref_RedTriangles.txt",
        f"{EXPDATA_DIR}/ZnO_Phonons_Ref_PurpleCircles.txt",
        f"{EXPDATA_DIR}/ZnO_Phonons_Ref_BlueSquares.txt",
    ]
    dfs_exp: list[pd.DataFrame] = [
        pd.read_csv(path, sep=";", header=2) for path in path_to_exp
    ]
    colors = ["red", "purple", "green"]
    markers = ["D", "o", "s"]
    labels_exp = ["Ref. 54", "Ref 55,56", "Ref 57"]

    # === PLOTTING ===

    # 1. Canvas
    fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
    fig.suptitle("LDA+U ALAMODE", fontsize=14, fontfamily="serif")

    # 2. Plotagem
    # Dados Teóricos frozen-phonons
    for i in range(freqs_thz.shape[1]):
        ax.plot(q_axis, freqs_thz[:, i], color="k", lw=1.5, zorder=3)

    # Dados Experimentais
    for i, df in enumerate(dfs_exp):
        ax.scatter(
            x=df["k"],
            y=df["Freq_THz"],
            marker=markers[i],
            color=colors[i],
            facecolors="none",
            linewidths=1.5,
            label=labels_exp[i],
            zorder=2,
        )
    # 3. Limites e Eixos
    ax.yaxis.set_major_locator(MultipleLocator(2))  # A cada 2 unidades.
    ax.yaxis.set_minor_locator(AutoMinorLocator(3))  # Divide o espaço de 2 em 3
    ax.tick_params(axis="y", which="major", direction="in", length=6, width=1.0)
    ax.tick_params(axis="y", which="minor", direction="in", length=3, width=1.0)
    ax.tick_params(axis="x", which="major", direction="inout", length=6, width=1.0)

    xticks, xtick_labels = get_brillouin_info(alamode_bands=alamode_bands)

    ax.set_xticks(xticks)
    # ax.set_yticks(np.arange(0, 21, 2))

    for x in xticks:
        ax.axvline(x, c="gray", alpha=0.5, ls="--")

    ax.set_xticklabels(xtick_labels, fontsize=14)
    ax.tick_params(axis="y", labelsize=14)

    ax.axhspan(ymin=0.0, ymax=-0.5, color="gray", alpha=0.3)

    # Limites e rótulos
    ax.set_xlim(q_axis.min(), q_axis.max())
    ax.set_ylim(freqs_thz.min() - 0.2, freqs_thz.max() + 1)
    ax.set_xlabel("")
    ax.set_ylabel("Frequência (ThZ)", fontsize=14, labelpad=10, fontfamily="serif")

    # Bordas
    for spine in ["top", "bottom", "left", "right"]:
        ax.spines[spine].set_linewidth(1.5)

    plt.savefig("phdisp-alamode_NA3.png", format="png", bbox_inches="tight")
    plt.tight_layout()
    plt.show()
