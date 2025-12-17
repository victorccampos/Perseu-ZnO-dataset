import matplotlib.pyplot as plt
import numpy as np

plt.style.use("/home/jvc/QEspresso7.2/ZnO_database/mpl_themes/jvc.mplstyle")


def plot_bands(
    gnuplot_filepath: str,
    high_sym_points: list[float],
    high_sym_labels: list[str],
    high_occ: float,
    lowest_unocc: float,
):
    """
    gnuplot_filepath is a ".gnu" created in post-processing with bands.x in the
    filband.

    The high_sym points and labels values can be extracted in the
    bands.x output.

    The high_occ and lowest_unocc can be extracted from pw.x scf calculation,
    after setting the nbnd.
    """
    bands = np.loadtxt(gnuplot_filepath)  # shape=(2592, 2)
    k = np.unique(bands[:, 0])

    bands = np.reshape(bands[:, 1], (-1, k.size))

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 5), dpi=600)

    ax.set_title("Estrutura de Bandas - LDA")
    ax.set_xlim(k.min(), k.max())
    ax.set_ylim([6, 18])
    ax.set_xticks(high_sym_points)
    # ax.set_yticks()
    ax.set_xticklabels(high_sym_labels)
    ax.set_xlabel("")
    ax.set_ylabel("Energia (eV)")

    ax.tick_params(axis="both", which="major", top=False, right=False)
    ax.tick_params(axis="both", which="minor", top=False, right=False)

    for band in range(len(bands)):
        ax.plot(k, bands[band, :], color="k")

    # Vertical Lines
    for value in high_sym_points:
        ax.axvline(value, color="gray", linestyle="--", alpha=0.5)

    # for value in [high_occ, lowest_unocc]:
    #     ax.axhline(value, color="red")

    gap = round((lowest_unocc - high_occ), 2)
    ax.axhspan(
        high_occ,
        lowest_unocc,
        zorder=3,
        hatch="xx",
        edgecolor="lightgray",
        facecolor="none",
        label=f"{gap} eV",
    )
    ax.grid(False)
    ax.legend()
    fig.tight_layout()
    fig.savefig("LDA_bandstructure.png", format="png", bbox_inches="tight")


if __name__ == "__main__":
    high_sym_points = [0.0000, 0.5774, 0.8888, 1.4661, 1.7776, 2.7958, 3.1072, 4.1255]
    high_sym_labels = [r"$\Gamma$", r"K", "L", "A", r"$\Gamma$", "K", "H", "A"]
    high_occ = 10.1075
    lowest_unocc = 10.9776

    plot_bands(
        gnuplot_filepath="ZnO_LDA_noU_bands.dat.gnu",
        high_sym_points=high_sym_points,
        high_sym_labels=high_sym_labels,
        high_occ=high_occ,
        lowest_unocc=lowest_unocc,
    )
