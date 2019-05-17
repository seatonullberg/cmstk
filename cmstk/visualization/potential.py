import type_sanity as ts
from cmstk.visualization.base import BasePlot
from cmstk.data.setfl import SetflReader


class SetflProfilePlot(BasePlot):
    """Implementation of a plot displaying embedding, density, and pair function curves.
    
    Args:
        reader (SetflReader): The setfl format eam potential reader.
    """

    def __init__(self, reader):
        ts.is_type((reader, SetflReader, "reader"))
        if reader._data is None:
            raise ValueError("`reader` must be populated prior to plotting")
        self._reader = reader
        super().__init__(nrows=1, ncols=3, figsize=(10, 5))  # construct 3 subplots

    def make(self):
        """Plots the available data.
        
        Args:
            None
        """
        # plot the embedding function for each symbol
        for e in self._reader.elements:
            embedding_y = self._reader.embedding_function(e)
            embedding_x = [self._reader.d_rho*(i+1) for i in range(self._reader.n_rho)]
            self.axes[0].plot(embedding_x, embedding_y, label=e)
            self.axes[0].legend()
            # these are defaults which can be overwritten
            self.axes[0].set_xlabel("Electron Density")
            self.axes[0].set_ylabel("Energy (eV)")
            self.axes[0].set_title("Embedding Function")

        # plot the density function for each symbol
        for e in self._reader.elements:
            density_y = self._reader.density_function(e)
            density_x = [self._reader.d_r*(i+1) for i in range(self._reader.n_r)]
            self.axes[1].plot(density_x, density_y, label=e)
            self.axes[1].legend()
            # these are defaults which can be overwritten
            self.axes[1].set_xlabel("Distance (Angstroms)")
            self.axes[1].set_ylabel("Electron Density")
            self.axes[1].set_title("Density Function")

        # plot the pair function for each pair
        for ep in self._reader.element_pairs:
            potential_y = self._reader.r_normalized_pair_function(ep)
            potential_x = [self._reader.d_r*(i+1) for i in range(self._reader.n_r)]
            self.axes[2].plot(potential_x, potential_y, label=ep)
            self.axes[2].legend()
            # these are defaults which can be overwritten
            self.axes[2].set_xlabel("Distance (Angstroms)")
            self.axes[2].set_ylabel("Energy (eV)")
            self.axes[2].set_title("Pair Function")

        self.fig.tight_layout(pad=1.0)
    