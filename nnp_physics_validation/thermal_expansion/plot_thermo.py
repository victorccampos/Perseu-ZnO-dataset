import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("../mestrado.mplstyle")


def plot_thermo(thermodat: str, **kwargs) -> None:

    header = "Step Temp Press Volume KinEng PotEng TotEng".split(" ")
    df = pd.DataFrame(np.loadtxt(thermodat), columns=header)
    fig, axes = plt.subplots(2, 2, figsize=(8, 5), dpi=300, sharex=True)
    ax_E, ax_V, ax_P, ax_T = axes.ravel()
    fig.suptitle(kwargs.get("figtitle", "Thermodynamic Outputs"))

    ax_titles = ["Energy", "Volume", "Pressure", "Temperature"]

    df.plot(x="Step", y="TotEng", ax=ax_E, rot=45, color="darkred")
    df.plot(x="Step", y="Volume", ax=ax_V, rot=45, color="darkgreen")
    df.plot(x="Step", y="Press", ax=ax_P, rot=45, color="darkblue")
    df.plot(x="Step", y="Temp", ax=ax_T, rot=45, color="darkblue")

    for i, ax in enumerate((ax_E, ax_V, ax_P, ax_T)):
        ax.set_title(ax_titles[i])
        ax.set_xlabel(r"MD Step ($10^3$)")
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x / 1e3)}"))
        ax.legend()
    line_config = dict(color="darkorange", lw=2, ls="--")
    ax_E.axhline(df["TotEng"].mean(), **line_config, label=r"$\langle E \rangle$")
    ax_P.axhline(df.Press.mean(), **line_config, label=r"$\langle P \rangle$")
    ax_V.axhline(df.Volume.mean(), **line_config, label=r"$\langle V \rangle$")
    ax_T.axhline(df.Temp.mean(), **line_config, label=r"$\langle V \rangle$")


    plt.savefig(f"{sys.argv[1]}".removesuffix(".dat") + ".png")
    plt.show()


if __name__ == "__main__":
    thermo: str = sys.argv[1]
    temperature: str = sys.argv[2]
    plot_thermo(sys.argv[1], figtitle=f"T = {temperature}K")
