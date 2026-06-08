import argparse
import numpy as np
import matplotlib.pyplot as plt

def read_bands(filename: str):
    """Lê o arquivo .bands do alamode

    Returns:
        - labels_fmt: list[str]   com pontos de alta simetria -> xtick labels
        - points    : list[float] com pontos de alta simetria -> xticks  
        - x         : list[float] com pontos da Zona de Brillouin (qi_s)
        - bands     : list[float] com as frequências
    """
    with open(filename, "r") as f:
        lines: list[str] = f.readlines()

    labels: list[str] = lines[0].strip().split()[1:]
    labels_fmt = [r"$\Gamma$" if label == "G" else label for label in labels]

    points = np.array(lines[1].strip().split()[1:], dtype=float)

    data = np.loadtxt(filename, comments="#")
    x = data[:, 0]
    bands = data[:, 1:]

    return labels_fmt, points, x, bands

def compare_bands(
    band_dft: np.ndarray, q_dft: np.ndarray, 
    band_mlff: np.ndarray, q_mlff: np.ndarray, 
    points: np.ndarray, labels: list, 
    ax: plt.Axes, **kwargs) -> plt.Axes:
    """Plota a comparação entre bandas DFT e MLFF"""
    
    title = kwargs.get('title')
    if title is not None:
       ax.set_title(title) 

    ax.set_xticks(points)
    ax.set_xticklabels(labels)
    
    ymin = min(band_dft.min(), band_mlff.min())
    ymax = max(band_dft.max(), band_mlff.max())
    
    ax.set_xlim([q_dft.min(), q_dft.max()])
    ax.set_ylim([ymin - 5, ymax + 20])

    ax.set_xlabel("")
    ax.set_ylabel(r"Frequency [cm$^{-1}$]")

    # Linhas de alta simetria
    for q in points:
        ax.axvline(q, color="gray", alpha=0.2, lw=0.5)

    # Bandas
    assert band_dft.shape == band_mlff.shape, "As bandas DFT e MLFF devem ter o mesmo shape"
    
    nbands = band_dft.shape[1]
    for q in range(nbands):
        ax.plot(q_dft, band_dft[:, q], color="k", ls="--", lw=2, label="DFT ALAMODE" if q == 0 else "")
        ax.plot(q_mlff, band_mlff[:, q], color="red", ls="-",lw=2, label="NNP" if q == 0 else "")

    ax.legend()

    return ax

def main():
    # Configuração do parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Compara a dispersão de fônons entre DFT e MLFF.")
    parser.add_argument("dft_bands", help="Caminho para o arquivo .bands de referência (DFT)")
    parser.add_argument("mlff_bands", help="Caminho para o arquivo .bands do modelo (MLFF/NNP)")
    parser.add_argument("-o", "--output", help="Opcional: Nome do arquivo para salvar a imagem (ex: plot.png)", default=None)
    
    args = parser.parse_args()

    # Leitura dos dados
    labels_dft, points_dft, q_dft, bands_dft = read_bands(args.dft_bands)
    _, _, q_mlff, bands_mlff = read_bands(args.mlff_bands)

    # Configuração da figura
    fig, ax = plt.subplots(figsize=(8, 6))

    # Comparação
    compare_bands(
        band_dft=bands_dft, q_dft=q_dft,
        band_mlff=bands_mlff, q_mlff=q_mlff,
        points=points_dft, labels=labels_dft, # Assumindo a malha geométrica da referência
        ax=ax, title="Phonon Dispersion: DFT vs NNP"
    )

    plt.tight_layout()

    # Salva ou exibe a imagem de acordo com o comando no terminal
    if args.output:
        plt.savefig(args.output, dpi=300, bbox_inches='tight')
        print(f"Plot salvo com sucesso em: {args.output}")
    else:
        plt.show()

if __name__ == "__main__":
    main()