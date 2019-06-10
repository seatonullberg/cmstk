import matplotlib.pyplot as plt
from cmstk.vasp.vasprun import VasprunReader


class DensityOfStatesPlot(object):
    """Implementation of a plot displaying DOS vs. Energy.
    
    Args:
        reader (VasprunReader): vasprun.xml reader to supply DOS data.
    """

    def __init__(self, reader):
        assert type(reader) is VasprunReader
        if reader._data is None:
            raise ValueError("`reader` must be populated prior to plotting")
        self._reader = reader
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))

    def make(self):
        """Plots the available data.
        
        Args:
            None
        """
        dos = self._reader.dos()
        e_fermi = self._reader.fermi_energy()
        energy = dos[:, 0]
        density = dos[:, 1]
        self.axes.plot(energy, density)
        self.axes.axvline(e_fermi, color="black")