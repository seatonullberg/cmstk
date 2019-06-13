from cmstk.base import BaseFile
from xml.etree import ElementTree
import numpy as np


class VasprunFile(BaseFile):
    """File wrapper for a VASP vasprun.xml file.
    
    Notes:
        This is a read-only file wrapper.

    Args:
        filepath (optional) (str): Filepath to a vasprun.xml file.
    """

    def __init__(self, filepath="vasprun.xml"):
        super().__init__(filepath)
        self._density_of_states = None
        self._eigenvalues = None
        self._fermi_energy = None

    def read(self, path=None):
        if path is None:
            path = self.filepath
        # Density of States
        root = ElementTree.parse(path).getroot()
        dos_tree = root.find("calculation").find("dos")
        arr = dos_tree.find("total")[0][-1][-1]
        dos = np.zeros(shape=(len(arr), 3))
        for i, row in enumerate(arr):
            for j in range(3):
                dos[i, j] = float(row.text.split()[j])
        self.density_of_states = dos
        # Eigenvalues
        try:
            ev_tree = root.find('calculation')\
                          .find('projected')\
                          .find('eigenvalues')\
                          .find('array')[-1]
        except AttributeError:
            ev_tree = root.find('calculation')\
                          .find('eigenvalues')\
                          .find('array')[-1]
        n_spins = len(ev_tree)
        n_kpoints = len(ev_tree[0])
        n_bands = len(ev_tree[0][0])
        eigenvalues = np.zeros(shape=(n_spins, n_kpoints, n_bands, 2))
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    eigenvalues[i, j, k, 0] = float(ev_tree[i][j][k].text
                                                                    .split()[0])
                    eigenvalues[i, j, k, 1] = float(ev_tree[i][j][k].text
                                                                    .split()[1])
        self._eigenvalues = eigenvalues
        # Fermi Energy
        fermi_energy = float(dos_tree.find("i").text)
        self._fermi_energy = fermi_energy

    @property
    def density_of_states(self):
        """(numpy.ndarray): Total density of states."""
        return self._density_of_states
    
    @density_of_states.setter
    def density_of_states(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        self._density_of_states = value

    @property
    def eigenvalues(self):
        """(numpy.ndarray): Array of eigenvalues of electrons in the system.
        - dimensionality: (n_spins, n_kpoints, n_bands, 2 <value, occupation>)
        """
        return self._eigenvalues

    @eigenvalues.setter
    def eigenvalues(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if len(value.shape) != 4:
            raise ValueError()
        self._eigenvalues = value

    @property
    def fermi_energy(self):
        """(float): Fermi energy of the system."""
        return self._fermi_energy

    @fermi_energy.setter
    def fermi_energy(self, value):
        if type(value) != float:
            raise TypeError()
        self._fermi_energy = value
