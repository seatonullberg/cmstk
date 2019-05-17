import type_sanity as ts
from cmstk.visualization.base import BasePlot
from cmstk.data.vasprun import VasprunReader


class DensityOfStatesPlot(BasePlot):
    """Implementation of a plot displaying DOS vs. Energy.
    
    Args:
        reader (VasprunReader): vasprun.xml reader to supply DOS data.
    """

    def __init__(self, reader):
        ts.is_type((reader, VasprunReader, "reader"))
        if reader._data is None:
            raise ValueError("`reader` must be populated prior to plotting")
        self._reader = reader
        super().__init__(nrows=1, ncols=1, figsize=(10, 5))  # construct a single subplot

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