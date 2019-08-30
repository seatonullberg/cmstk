import matplotlib.pyplot as plt
from cmstk.eam import SetflFile


class SetflProfilePlot(object):
    """Implementation of a plot displaying embedding, density, and pair function curves.
    
    Args:
        reader (SetflReader): The setfl format eam potential reader.
    """
    def __init__(self, setfl):
        assert type(setfl) is SetflFile
        self._setfl = setfl
        self.fig, self.axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 5))

    def make(self):
        """Plots the available data.
        
        Args:
            None
        """
        # plot the embedding function for each symbol
        for s in self._setfl.symbols:
            embedding_y = self._setfl.embedding_function[s]
            embedding_x = [
                self._setfl.d_rho * (i + 1) for i in range(self._setfl.n_rho)
            ]
            self.axes[0].plot(embedding_x, embedding_y, label=s)
            self.axes[0].legend()
            # these are defaults which can be overwritten
            self.axes[0].set_xlabel("Electron Density")
            self.axes[0].set_ylabel("Energy (eV)")
            self.axes[0].set_title("Embedding Function")

        # plot the density function for each symbol
        for s in self._setfl.symbols:
            density_y = self._setfl.density_function[s]
            density_x = [
                self._setfl.d_r * (i + 1) for i in range(self._setfl.n_r)
            ]
            self.axes[1].plot(density_x, density_y, label=s)
            self.axes[1].legend()
            # these are defaults which can be overwritten
            self.axes[1].set_xlabel("Distance (Angstroms)")
            self.axes[1].set_ylabel("Electron Density")
            self.axes[1].set_title("Density Function")

        # plot the pair function for each pair
        for sp in self._setfl.symbol_pairs:
            #potential_y = self._setfl.r_normalized_pair_function[sp]
            potential_y = self._setfl.pair_function[sp]
            potential_x = [
                self._setfl.d_r * (i + 1) for i in range(self._setfl.n_r)
            ]
            self.axes[2].plot(potential_x, potential_y, label=sp)
            self.axes[2].legend()
            # these are defaults which can be overwritten
            self.axes[2].set_xlabel("Distance (Angstroms)")
            self.axes[2].set_ylabel("Energy (eV)")
            self.axes[2].set_title("Pair Function")

        self.fig.tight_layout(pad=1.0)
