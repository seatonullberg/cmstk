from cmstk.data.setfl import SetflReader
import matplotlib.pyplot as plt


class SetflProfilePlot(object):
    """Represents a plotting object which produces embedding, density, and interatomic potential curves from a SetflReader.
    
    Args:
        reader (SetflReader): The setfl format eam potential reader object.
    """

    def __init__(self, reader):
        if type(reader) is not SetflReader:
            raise TypeError("`reader` must be of type SetflReader")
        self._reader = reader

    def generate_plot(self):
        fig, axes = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True)
        # plot the embedding function for each symbol
        for e in self._reader.elements:
            embedding_y = self._reader.embedding_function(e)
            embedding_x = [self._reader.d_rho*(i+1) for i in range(self._reader.n_rho)]
            axes[0].scatter(embedding_x, embedding_y, s=1)
            axes[0].set_title("Embedding Function")
        # plot the density function for each symbol
        for e in self._reader.elements:
            density_y = self._reader.density_function(e)
            density_x = [self._reader.d_r*(i+1) for i in range(self._reader.n_r)]
            axes[1].scatter(embedding_x, embedding_y, s=1)
            axes[1].set_title("Density Function")
        # plot the interatomic potential function for each pair
        for ep in self._reader.element_pairs:
            potential_y = self._reader.interatomic_potential(ep)
            potential_x = [self._reader.d_r*(i+1) for i in range(self._reader.n_r)]
            axes[2].scatter(potential_x, potential_y, s=1)
            axes[2].set_title("Interatomic Potential")

        plt.show()