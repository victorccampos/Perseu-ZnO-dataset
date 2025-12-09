"""
Python script to plot ZnO Phonon Dispersion.
The required data is a gnuplot style "ZnO.freq.gp"
The brillouin path is: gG - K - M - G - A - H - H
Each points is interpolated with 40 points. (hardcoded in code below)
"""
import ase.units
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_phonon_data(gnuplot_datfile: str):
    lines = []
    with open(gnuplot_datfile) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                lines.append(line)
    data = np.loadtxt(lines)

    return data


if __name__ == "__main__":
    # Dados do arquivo QE
    data = get_phonon_data("ZnO.freq.gp")
    q = data[:, 0]
    freqs_invcm = data[:, 1:]

    # Conversão unidades
    invcm_to_thz = 0.029979
    invcm_to_mev = ase.units.invcm * 1_000

    freqs_mev = freqs_invcm * invcm_to_mev
    freqs_thz = freqs_invcm * invcm_to_thz

    # Dados experimentaisD
    EXP_DIR = "../phononDFPT_U/phonon-experimental-data-meV"
    path_to_exp: list[str] = [
        f"{EXP_DIR}/expdata_red_squares.csv",
        f"{EXP_DIR}/expdata_purple_circles.csv",
        f"{EXP_DIR}/expdata_green_squares.csv",
    ]
    columns = ["k", "freq_meV"]
    dfs_exp = [pd.read_csv(path, names=columns, delimiter=";") for path in path_to_exp]

    # Plotting
    plot_theme = "/home/jvc/QEspresso7.2/ZnO_database/mpl_themes/sci.mplstyle"
    plt.style.use(plot_theme)
    plt.figure(dpi=600)
    plt.title("LDA", fontsize=14)
    high_symmetry_points = [q[40 * i] for i in range(7)]
    high_symmetry_labels = [
        r"$\Gamma$",
        r"$K$",
        r"$M$",
        r"$\Gamma$",
        r"$A$",
        r"$H$",
        r"$K$",
    ]
    # QE - DFPT
    for i in range(freqs_mev.shape[1]):
        plt.plot(q, freqs_mev[:, i], lw=1.5, color="k")

    # Experimental
    markers = ["D", "o", "s"]
    colors = ["red", "purple", "green"]
    idf = 0
    for df in dfs_exp:
        plt.scatter(
            df["k"],
            df["freq_meV"],
            marker=markers[idf],
            color=colors[idf],
            facecolors="none",
        )
        idf += 1

    for hsp in high_symmetry_points:
        plt.axvline(hsp, c="gray", alpha=0.3, ls=":")

    plt.ylabel("Frequency (meV)", labelpad=10, fontsize=14)
    plt.xlabel("")

    plt.xticks(ticks=high_symmetry_points, labels=high_symmetry_labels, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(high_symmetry_points[0], high_symmetry_points[-1])
    plt.ylim([-0.5, np.max(freqs_mev) + 10.0])

    plt.tight_layout()
    # plt.savefig("phonondisp_vs_exp-LDA.png", format="png")
    plt.savefig("phonondisp_vs_exp-LDA.pdf", format="pdf")
    plt.show()
