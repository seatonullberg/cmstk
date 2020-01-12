import matplotlib.pyplot as plt
from cmstk.eam import SetflFile
from typing import Tuple


def setfl_profile_plot(setfl: SetflFile) -> Tuple[plt.Figure, plt.Axes]:
    """Prepares a plot displaying the attributes of an EAM potential.

    Args:
        setfl: SetflFile object to pull EAM information from.
    """
    fig, axes = plt.subplots(nrows=1, ncols=3)
    # plot the embedding function for each symbol
    for s in setfl.symbols:
        embedding_y = setfl.embedding_function[s]
        embedding_x = [setfl.d_rho * (i + 1) for i in range(setfl.n_rho)]
        axes[0].plot(embedding_x, embedding_y, label=s)
        axes[0].legend()
        axes[0].set_xlabel("Electron Density")
        axes[0].set_ylabel("Energy (eV)")
        axes[0].set_title("Embedding Function")
    # plot the density function for each symbol
    for s in setfl.symbols:
        density_y = setfl.density_function[s]
        density_x = [setfl.d_r * (i + 1) for i in range(setfl.n_r)]
        axes[1].plot(density_x, density_y, label=s)
        axes[1].legend()
        axes[1].set_xlabel("Distance (Angstroms)")
        axes[1].set_ylabel("Electron Density")
        axes[1].set_title("Density Function")
    # plot the pair function for each pair
    for sp in setfl.symbol_pairs:
        potential_y = setfl.pair_function[sp]
        potential_x = [setfl.d_r * (i + 1) for i in range(setfl.n_r)]
        axes[2].plot(potential_x, potential_y, label=sp)
        axes[2].legend()
        axes[2].set_xlabel("Distance (Angstroms)")
        axes[2].set_ylabel("Energy (eV)")
        axes[2].set_title("Pair Function")
    fig.tight_layout(pad=1.0)
    return (fig, axes)
