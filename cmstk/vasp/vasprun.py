from xml.etree import ElementTree
import numpy as np
from typing import Optional, Sequence


class VasprunFile(object):
    """File wrapper for a VASP vasprun.xml file.
    
    Notes:
        This is a read-only file wrapper.

    Args:
        filepath (optional) (str): Filepath to a vasprun.xml file.

    Attributes:
        filepath (optional) (str): Filepath to a vasprun.xml file.
        density_of_states (numpy.ndarray): Total density of states.
        eigenvalues (numpy.ndarray): Array of eigenvalues of electrons in the 
        system.
        - dimensionality: (n_spins, n_kpoints, n_bands, 2 <value, occupation>)
        fermi_energy (float): Fermi energy of the system.
    """

    def __init__(self, filepath: str = "vasprun.xml") -> None:
        self.filepath = filepath
        self.density_of_states: np.ndarray
        self.eigenvalues: np.ndarray
        self.fermi_energy: float

    def read(self, path: Optional[str] = None) -> None:
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
        self.eigenvalues = eigenvalues
        # Fermi Energy
        fermi_energy = float(dos_tree.find("i").text)
        self.fermi_energy = fermi_energy
