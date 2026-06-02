import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_training(trainerror: str) -> pd.DataFrame:
    errors  = np.loadtxt(trainerror)
    names = ["epoch", "error_train", "error_test", "E_train", "E_test", "F_train", "F_test"]
    df = pd.DataFrame(data=errors, columns=names)
    df['epoch'] = df['epoch'].astype(int)
    
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 5), layout="constrained")
    fig.suptitle("Training curves")
    
    plots = [
            (["error_train", "error_test"], "Total Error"),
            (["E_train", "E_test"], "Energy Error"),
            (["F_train", "F_test"], "Force Error"),
        ]
    
    colors = ["black", "red"]
    
    for i, (cols, title) in enumerate(plots):
        # Escala normal        
        df[cols].plot(ax=axes[0, i], title=title, color=colors)
        # Log-plot
        df[cols].plot(
            ax=axes[1, i],
            title=f"{title} (Log)",
            logy=True,
            logx=True,
            color=colors,
        )
    # Metrics in meV/atom for energy and meV/Å for forces
    min_E_train = df['E_train'].min()  * 1_000
    min_E_test  = df['E_test'].min()   * 1_000
    
    min_F_train = df['F_train'].min() 
    min_F_test  = df['F_test'].min() 

    # Epochs corresponding to the minimum values
    epoch_min_E_train = df.loc[df['E_train'].idxmin(), 'epoch']
    epoch_min_E_test = df.loc[df['E_test'].idxmin(), 'epoch']
    epoch_min_F_train = df.loc[df['F_train'].idxmin(), 'epoch']
    epoch_min_F_test = df.loc[df['F_test'].idxmin(), 'epoch']

    # Annotating min metrics with corresponding epochs, in center of the corresponing axes
    text_kwargs = dict(ha='center', va='center', fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    # Texts to display, energy in meV/atom and forces in meV/Å
    text_E = f"Min E_train: {min_E_train:.2f} at epoch {epoch_min_E_train}\nMin E_test: {min_E_test:.2f} at epoch {epoch_min_E_test}"
    text_F = f"Min F_train: {min_F_train:.2f} at epoch {epoch_min_F_train}\nMin F_test: {min_F_test:.2f} at epoch {epoch_min_F_test}"

    axes[0, 1].text(0.5, 0.5, text_E, transform=axes[0, 1].transAxes, **text_kwargs)
    axes[0, 2].text(0.5, 0.5, text_F, transform=axes[0, 2].transAxes, **text_kwargs)

    plotname = trainerror.replace(".error", ".png")
    fig.savefig(fname=plotname, dpi=600, bbox_inches='tight')
    return df



if __name__ == '__main__':
    df = plot_training("train.error")
    print(df)
