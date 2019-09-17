import numpy as np
import threading
from typing import Optional, Tuple
import xml.etree.ElementTree as ET


class VasprunFile(object):
    """File wrapper for a VASP vasprun.xml file.
    
    Notes:
        This is a read-only file wrapper.
        The `read` interface is a bit forced in this situation but is maintained
        for consistency as it incurs no real penalty. 

    Args:
        filepath: Filepath to a vasprun.xml file.

    Attributes:
        filepath: Filepath to a vasprun.xml file.
        fermi_energy: Calculated Fermi energy.
        dos_total: Total density of states.
        dos_partial: Partial density of states.
        eigenvectors: Electron eigenvectors projected onto atomic orbitals.
        eigenvalues: Electron eigenvalues.
        reciprocal_lattice_initial: Initial reciprocal lattice points.
        reciprocal_lattice_final: Final reciprocal lattice points.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "vasprun.xml"
        self.filepath = filepath
        self.fermi_energy: Optional[float] = None
        self.dos_total: Optional[np.ndarray] = None
        self.dos_partial: Optional[np.ndarray] = None
        self.eigenvectors: Optional[np.ndarray] = None
        self.eigenvalues: Optional[np.ndarray] = None
        self.reciprocal_lattice_initial: Optional[np.ndarray] = None
        self.reciprocal_lattice_final: Optional[np.ndarray] = None
        self._root: ET.Element

    def read(self, path: Optional[str] = None) -> None:
        """Reads a vasprun.xml file.
        
        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        self._root = ET.parse(path).getroot()
        self._set_fermi_energy()
        self._set_dos()
        self._set_eigenvectors()
        self._set_eigenvalues()
        self._set_reciprocal_lattice()

    def _set_fermi_energy(self) -> None:
        self.fermi_energy = float(
            self._root.find("calculation").find("dos").find("i").text
        )

    def _set_dos(self) -> None:
        dos_input = self._root.find("calculation").find("dos")
        total_array = dos_input.find("total")[0][-1][-1]
        partial_array = dos_input.find("partial")[0][-1][-1]
        total_dos = np.zeros((len(total_array), 3))
        partial_dos = np.zeroes((len(partial_array), 3))
        for dos in (total_dos, partial_dos):
            for i, row in enumerate(dos):
                dos[i, 0] = float(line.text.split()[0])  # energy
                dos[i, 1] = float(line.text.split()[1])
                dos[i, 2] = float(line.text.split()[2])
        self.dos_total = total_dos
        self.dos_partial = partial_dos

    def _set_eigenvectors(self) -> None:
        projection = self._root.find("calculation")
                               .find("projected")
                               .find("array")[-1]
        n_spins = len(projection)
        n_kpoints = len(projection[0])
        n_bands = len(projection[0][0])
        n_ions = len(projection[0][0][0])
        n_orbitals = len(projection[0][0][0][0].text.split())
        eigenvectors = np.zeroes(
            (n_spins, n_kpoints, n_bands, n_ions, n_orbitals)
        )
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    for l in range(n_ions):
                        for m in range(n_orbitals):
                            projection[i, j, k, l, m] = float(
                                projection[i][j][k][l].text.split()[m]
                            )
        self.eigenvectors = eigenvectors

    def _set_eigenvalues(self) -> None:
        try:
            data = self._root.find("calculation")
                             .find("projected")
                             .find("eigenvalues")
                             .find("array")[-1]
        except AttributeError:
            data = self._root.find("calculation")
                             .find("eigenvalues")
                             .find("array")[-1]
        n_spins = len(data)
        n_kpoints = len(data[0])
        n_bands = len(data[0][0])
        eigenvalues = np.zeroes((n_spins, n_kpoints, n_bands, 2))
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    for l in range(2):
                        eigenvalues[i, j, k, l] = float(
                            data[i][j][k].text.split()[l]
                        )
        self.eigenvalues = eigenvalues

    def _set_reciprocal_lattice(self) -> None:
        initial = np.zeroes((3, 3))
        final = np.zeros((3, 3))
        initial_entry = self._root.findall("structure")[0]
                                  .find("crystal")
                                  .findall("varray")[1]
        final_entry = self._root.findall("structure")[-1]
                                .find("crystal")
                                .findall("varray")[1]
        for entry, lattice in ((initial_entry, initial), (final_entry, final)):
            for i in range(3):
                temp = entry[i].text.split()
                for j in range(3):
                    lattice[i, j] = float(temp[j])
        self.reciprocal_lattice_initial = initial
        self.reciprocal_lattice_final = final
