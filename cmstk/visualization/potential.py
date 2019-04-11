from cmstk.data.setfl import SetflReader
import matplotlib.pyplot as plt


class SetflProfilePlot(object):
    """Represents a plotting object which produces embedding, density, and pair function curves from a SetflReader.
    
    Args:
        reader (SetflReader): The setfl format eam potential reader object.
    """

    def __init__(self, reader):
        if type(reader) is not SetflReader:
            raise TypeError("`reader` must be of type SetflReader")
        self._reader = reader

    def generate_plot(self, filename):
        """Generates and saves plot to file.
        
        Args:
            filename (str): File path to write the plot to.
        """
        if type(filename) is not str:
            raise TypeError("`filename` must be of type str")
        
        fig, axes = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=False, figsize=(10,5))
        # plot the embedding function for each symbol
        for e in self._reader.elements:
            embedding_y = self._reader.embedding_function(e)
            embedding_x = [self._reader.d_rho*(i+1) for i in range(self._reader.n_rho)]
            axes[0].plot(embedding_x, embedding_y, label=e)
            axes[0].set_xlabel("Distance (Angstroms)")
            axes[0].set_ylabel("Energy (eV)")
            axes[0].set_title("Embedding Function")
            axes[0].legend()
        # plot the density function for each symbol
        for e in self._reader.elements:
            density_y = self._reader.density_function(e)
            density_x = [self._reader.d_r*(i+1) for i in range(self._reader.n_r)]
            axes[1].plot(density_x, density_y, label=e)
            axes[1].set_xlabel("Distance (Angstroms)")
            axes[1].set_ylabel("Electron Density")
            axes[1].set_title("Density Function")
            axes[1].legend()
        # plot the pair function for each pair
        for ep in self._reader.element_pairs:
            potential_y = self._reader.pair_function(ep)
            potential_x = [self._reader.d_r*(i+1) for i in range(self._reader.n_r)]
            axes[2].plot(potential_x, potential_y, label=ep)
            axes[2].set_xlabel("Distance (Angstroms)")
            axes[2].set_ylabel("Energy (eV)")
            axes[2].set_title("Pair Function")
            axes[2].legend()
        plt.tight_layout(pad=1.0)
        plt.savefig(filename)
    