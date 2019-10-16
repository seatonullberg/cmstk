import numpy as np
import threading
from typing import Optional, Tuple
import xml.etree.ElementTree as ET
# This file effectively ignores all type hints because handling them while
# parsing XML is a massive hassle


class VasprunFile(object):
    """File wrapper for a VASP vasprun.xml file.
    
    Notes:
        This wrapper does not follow the same `read` `write` interface as the
        others because the information available for parsing varies depending on
        the type of calculation. 

    Args:
        filepath: Filepath to a vasprun.xml file.

    Attributes:
        filepath: Filepath to a vasprun.xml file.
    """
    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "vasprun.xml"
        self.filepath = filepath
        self._root = ET.parse(self.filepath).getroot()

    def density_of_states(self) -> np.ndarray:
        """Returns the total density of states."""
        flag = "total"
        dos_input = self._root.find("calculation").find("dos").find(
            flag)[0][-1][-1]  # type: ignore
        dos = np.zeros((len(dos_input), 3))
        for i, row in enumerate(dos_input):
            dos[i, 0] = float(row.text.split()[0])  # energy
            dos[i, 1] = float(row.text.split()[1])
            dos[i, 2] = float(row.text.split()[2])
        return dos

    def eigenvalues(self) -> np.ndarray:
        try:
            data = self._root.find("calculation").find("projected").find(
                "eigenvalues").find("array")[-1]  # type: ignore
        except AttributeError:
            data = self._root.find("calculation").find("eigenvalues").find(
                "array")[-1]  # type: ignore
        n_spins = len(data)
        n_kpoints = len(data[0])
        n_bands = len(data[0][0])
        eigenvalues = np.zeros((n_spins, n_kpoints, n_bands, 2))
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    for l in range(2):
                        eigenvalues[i, j, k, l] = float(
                            data[i][j][k].text.split()[l]  # type: ignore
                        )
        return eigenvalues

    def eigenvectors(self) -> np.ndarray:
        """Returns the electron eigenvectors projected onto atomic orbitals."""
        projection = self._root.find("calculation").find("projected").find(
            "array")[-1]  # type: ignore
        n_spins = len(projection)
        n_kpoints = len(projection[0])
        n_bands = len(projection[0][0])
        n_ions = len(projection[0][0][0])
        n_orbitals = len(projection[0][0][0][0].text.split())  # type: ignore
        eigenvectors = np.zeros(
            (n_spins, n_kpoints, n_bands, n_ions, n_orbitals))
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    for l in range(n_ions):
                        for m in range(n_orbitals):
                            eigenvectors[i, j, k, l, m] = float(
                                projection[i][j][k][l].text.split()
                                [m])  # type: ignore
        return eigenvectors

    def fermi_energy(self) -> float:
        """Returns the calculated fermi energy."""
        return float(
            self._root.find("calculation").find("dos").find(
                "i").text)  # type: ignore

    def reciprocal_lattice(self, initial: bool = True) -> np.ndarray:
        """Returns the initial or final reciprocal lattice vectors.
        
        Args:
            initial: Bool flag to determine initial or final lattice vectors.
        """
        index = (0 if initial else -1)
        lattice = np.zeros((3, 3))
        lattice_entry = self._root.findall("structure")[index].find(
            "crystal").findall("varray")[1]  # type: ignore
        for i in range(3):
            temp = lattice_entry[i].text.split()  # type: ignore
            for j in range(3):
                lattice[i, j] = float(temp[j])
        return lattice
