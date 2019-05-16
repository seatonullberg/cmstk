import type_sanity as ts
import numpy as np
from cmstk.data.base import BaseDataReader


class VasprunReader(BaseDataReader):
    """Represents access to VASP output file `vasprun.xml`.
    
    Args:
        filename (str): Filename to read.
    """

    def __init__(self, filename):
        ts.is_type((filename, str, "filename"))
        super().__init__()
        self.read_xml(filename)

    def dos(self, total=True):
        """Returns an array of the density of states at all energy levels.
        
        Args:
            total (optional) (bool): Determines whether `total` or `partial` is extracted.
        
        Returns:
            numpy.ndarray
            - col 0: energy
            -col 1, 2: density
        """
        dos_section = self._data.find("calculation").find("dos")
        if total:
            arr = dos_section.find("total")
        else:
            arr = dos_section.find("partial")
        arr = arr[0][-1][-1]
        result = np.zeros(shape=(len(arr), 3))
        for i, row in enumerate(arr):
            for j in range(3):
                result[i, j] = float(row.text.split()[j])
        return result

    def eigenvalues(self):
        """Returns an array of the electron Eigenvalues.
        
        Returns:
            numpy.ndarray
            - dimensionality = (n_spins, n_kpoints, n_bands, 2 <value, occupation>)
        """
        try:
            eigen = self._data.find('calculation').find('projected').find('eigenvalues').find('array')[-1]
        except AttributeError:
            eigen = self._data.find('calculation').find('eigenvalues').find('array')[-1]

        n_spins, n_kpoints, n_bands = len(eigen), len(eigen[0]), len(eigen[0][0])
        evalues = np.zeros(shape=(n_spins, n_kpoints, n_bands, 2))
        for i in range(n_spins):
            for j in range(n_kpoints):
                for k in range(n_bands):
                    evalues[i, j, k, 0] = float(eigen[i][j][k].text.split()[0])
                    evalues[i, j, k, 1] = float(eigen[i][j][k].text.split()[1])
        return evalues

    def fermi_energy(self):
        """Returns the Fermi-Energy.
        
        Returns:
            float
        """
        dos_section = self._data.find("calculation").find("dos")
        e_fermi = float(dos_section.find("i").text)
        return e_fermi
