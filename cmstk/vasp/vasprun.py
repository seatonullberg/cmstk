import numpy as np
from typing import Optional
import xml.etree.ElementTree as ET

_bad_xml_err = "Unable to find or parse section `{}`."


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
        density_of_states: Total density of states.
        eigenvalues: Projected or actual eigenvalues. 
        eigenvectors: Electron eigenvectors projected onto atomic orbitals.
        fermi_energy: The calculated Fermi Energy.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "vasprun.xml"
        self.filepath = filepath
        self._root = ET.parse(self.filepath).getroot()

    @property
    def density_of_states(self) -> np.ndarray:
        dos_input = self._root.find("calculation")
        if dos_input is None:
            err = _bad_xml_err.format("calculation")
            raise ValueError(err)
        dos_input = dos_input.find("dos")
        if dos_input is None:
            err = _bad_xml_err.format("dos")
            raise ValueError(err)
        dos_input = dos_input.find("total")
        if dos_input is None:
            err = _bad_xml_err.format("total")
            raise ValueError(err)
        dos_input = dos_input[0][-1][-1]
        dos = np.zeros((len(dos_input), 3))
        for i, row in enumerate(dos_input):
            text = row.text
            if text is None:
                err = _bad_xml_err.format("total")
                raise ValueError(err)
            dos[i, 0] = float(text.split()[0])  # energy
            dos[i, 1] = float(text.split()[1])
            dos[i, 2] = float(text.split()[2])
        return dos

    @property
    def eigenvalues(self) -> np.ndarray:
        data = self._root.find("calculation")
        if data is None:
            err = _bad_xml_err.format("calculation")
            raise ValueError(err)
        is_projected = True
        try:
            _ = data.find("projected")
        except AttributeError:
            is_projected = False
        if is_projected:
            data = data.find("projected")
            if data is None:
                err = _bad_xml_err.format("projected")
                raise ValueError(err)
        data = data.find("eigenvalues")
        if data is None:
            err = _bad_xml_err.format("eigenvalues")
            raise ValueError(err)
        data = data.find("array")
        if data is None:
            err = _bad_xml_err.format("array")
            raise ValueError(err)
        data = data[-1]
        n_spins = len(data)
        n_kpoints = len(data[0])
        n_bands = len(data[0][0])
        eigenvalues = np.zeros((n_spins, n_kpoints, n_bands, 2))
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    for l in range(2):
                        text = data[i][j][k].text
                        if text is None:
                            err = _bad_xml_err.format("array")
                            raise ValueError(err)
                        eigenvalues[i, j, k, l] = float(text.split()[l])
        return eigenvalues

    @property
    def eigenvectors(self) -> np.ndarray:
        projection = self._root.find("calculation")
        if projection is None:
            err = _bad_xml_err.format("calculation")
            raise ValueError(err)
        projection = projection.find("projected")
        if projection is None:
            err = _bad_xml_err.format("projected")
            raise ValueError(err)
        projection = projection.find("array")
        if projection is None:
            err = _bad_xml_err.format("array")
            raise ValueError(err)
        projection = projection[-1]
        n_spins = len(projection)
        n_kpoints = len(projection[0])
        n_bands = len(projection[0][0])
        n_ions = len(projection[0][0][0])
        text = projection[0][0][0][0].text
        if text is None:
            err = _bad_xml_err.format("array")
            raise ValueError(err)
        n_orbitals = len(text.split())
        eigenvectors = np.zeros(
            (n_spins, n_kpoints, n_bands, n_ions, n_orbitals))
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    for l in range(n_ions):
                        for m in range(n_orbitals):
                            text = projection[i][j][k][l].text
                            if text is None:
                                err = _bad_xml_err.format("array")
                                raise ValueError(err)
                            eigenvectors[i, j, k, l, m] = float(text.split()[m])
        return eigenvectors

    @property
    def fermi_energy(self) -> float:
        fermi = self._root.find("calculation")
        if fermi is None:
            err = _bad_xml_err.format("calculation")
            raise ValueError(err)
        fermi = fermi.find("dos")
        if fermi is None:
            err = _bad_xml_err.format("dos")
            raise ValueError(err)
        fermi = fermi.find("i")
        if fermi is None:
            err = _bad_xml_err.format("i")
            raise ValueError(err)
        text = fermi.text
        if text is None:
            err = _bad_xml_err.format("i")
            raise ValueError(err)
        return float(text)
