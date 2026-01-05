"""
Script python gera dispersão fonônica DFPT e compara com dados experimentais.
Lê ZnO.freq.gp, converte frequências de cm⁻¹ para meV (eixo y principal) e plota
todas as bandas.

Carrega três séries experimentais (expdata_*) e as sobrepõe como marcadores coloridos.
Define pontos e rótulos de simetria alta (Γ–K–M–Γ–A–H–K) e desenha linhas verticais neles.
"""

import ase.units
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import pandas as pd


# CONVERSÃO UNIDADES
INV_CM_TO_THZ = 0.029979
INV_CM_TO_MEV = ase.units.invcm * 1_000


def invcm2meV(freq_invcm):
    return freq_invcm * INV_CM_TO_MEV


def invcm2THz(freq_invcm):
    return freq_invcm * INV_CM_TO_THZ


def meV2THz(freq_mev):
    freq_invcm = freq_mev / INV_CM_TO_MEV
    return invcm2THz(freq_invcm)


def THz2meV(freq_thz):
    freq_invcm = freq_thz / INV_CM_TO_THZ
    return invcm2meV(freq_invcm)


def load_qe_freqs(gnuplot_datfile: str):
    """
    Lê o arquivo .gp do Quantum ESPRESSO com frequências em cm^-1
    """
    lines = []
    with open(gnuplot_datfile) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                lines.append(line)
    data = np.loadtxt(lines)
    q = data[:, 0]
    freqs_invcm = data[:, 1:]

    freqs_mev = invcm2meV(freqs_invcm)
    return q, freqs_mev


def load_experimental(paths: list[str]) -> list[pd.DataFrame]:
    return [pd.read_csv(p, names=["k", "freq_meV"], delimiter=";") for p in paths]


def plot_phonons(
    title: str,
    q: np.ndarray,
    freqs_mev: np.ndarray,
    dfs_exp: list[pd.DataFrame],
    high_symmetry_points: list[float],
    high_symmetry_labels: list[str],
    image_output: str,
):
    """
    Plota a dispersão de fônons (DFT/DFPT + dados experimentais) com eixo
    secundátio em THz
    """

    fig, ax = plt.subplots(figsize=(6, 5), dpi=600)
    ax.set_title(title, pad=10)

    # -------------------------
    # 1. DFPT (curvas)
    for i in range(freqs_mev.shape[1]):
        ax.plot(q, freqs_mev[:, i], lw=1.5, color="k", zorder=2)

    # -------------------------
    # 2. Dados experimentais
    markers = ["D", "o", "s"]
    colors = ["red", "purple", "green"]

    for df, m, c in zip(dfs_exp, markers, colors):
        ax.scatter(
            df["k"],
            df["freq_meV"],
            marker=m,
            color=c,
            facecolors="none",
            linewidths=1.5,
            zorder=3,
        )

    # -------------------------
    # 3. Linhas verticais: pontos de alta simetria
    for hsp in high_symmetry_points:
        ax.axvline(hsp, c="gray", alpha=0.5, ls="--")

    # -------------------------
    # 4. Eixos principais
    ax.set_ylabel("Frequência (meV)", labelpad=10)
    ax.set_xlabel("")
    ax.set_xlim(high_symmetry_points[0], high_symmetry_points[-1])
    ax.set_ylim([0, 80])
    ax.set_xticks(ticks=high_symmetry_points, labels=high_symmetry_labels)

    # Ticks Y em meV
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.tick_params(
        axis="y", which="major", direction="in", length=6, width=1.0, right=False
    )
    ax.tick_params(
        axis="y", which="minor", direction="in", length=3, width=1.0, right=False
    )
    ax.tick_params(axis="x", which="major", direction="in", length=6, width=1.0)

    # -------------------------
    # 5. Eixo secundário em THz
    secax = ax.secondary_yaxis("right", functions=(meV2THz, THz2meV))
    secax.set_ylabel("Frequência (THz)")
    secax.set_ylim([0, 22])
    secax.yaxis.set_major_locator(MultipleLocator(2))
    secax.yaxis.set_minor_locator(AutoMinorLocator(5))

    # -------------------------
    plt.tight_layout()
    plt.savefig(image_output, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plt.style.use("/home/jvc/ZnO_database/mpl_themes/jvc.mplstyle")
    # Path to data
    QE_FREQS_PATH = "ZnO.freq.gp"
    EXP_DIR = (
        "/home/jvc/ZnO_database/DFT_LDAU/phononDFPT_U/phonon-experimental-data-meV"
    )

    path_to_exp: list[str] = [
        f"{EXP_DIR}/expdata_red_squares.csv",
        f"{EXP_DIR}/expdata_purple_circles.csv",
        f"{EXP_DIR}/expdata_green_squares.csv",
    ]

    q, freqs_mev = load_qe_freqs(gnuplot_datfile=QE_FREQS_PATH)
    dfs_exp = load_experimental(paths=path_to_exp)

    # Plotting
    gG = r"$\Gamma$"
    high_symmetry_labels = [gG, "K", "M", gG, "A", "H", "K"]
    high_symmetry_points = [q[40 * i] for i in range(len(high_symmetry_labels))]

    plot_phonons(
        title="PBE DFPT",
        q=q,
        freqs_mev=freqs_mev,
        dfs_exp=dfs_exp,
        high_symmetry_points=high_symmetry_points,
        high_symmetry_labels=high_symmetry_labels,
        image_output="ZnO_phonons_PBE_DFPT_vs_experimental.png",
    )
