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

    def dos(self, is_total=True):
        """Returns an array of the density of states at all energy levels.
        
        Args:
            is_total (optional) (bool): Determines whether `total` or `partial` DOS is extracted.
        
        Returns:
            numpy.ndarray
            - col 0: energy
            -col 1, 2: density
        """
        ts.is_type((is_total, bool, "is_total"))
        dos_section = self._data.find("calculation").find("dos")
        if is_total:
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

    def kpoints(self):
        """Returns an array of the k-points.
        
        Returns:
            numpy.ndarray
        """
        kpts_raw = self._data.find('kpoints').findall('varray')[0]
        n_kpts = len(kpts_raw)
        kpts = np.zeros(shape=(n_kpts, 3))
        for i in range(n_kpts):
            for j in range(3):
                kpts[i, j] = float(kpts_raw[i].text.split()[j])
        return kpts

    def kpoints_path(self):
        """Returns the k-points generation path.
        
        Returns:
            numpy.ndarray
        """
        generation = self._data.find('kpoints').find('generation').findall('v')
        kpath = np.zeros([len(generation), 3])
        for i in range(len(generation)):
            for j in range(3):
                kpath[i, j] = float(generation[i].text.split()[j])
        return kpath

    def reciprocal_lattice(self, is_initial=True):
        """Returns lattice vectors of the reciprocal lattice.
        
        Args:
            is_initial (optional) (bool): Determines if the initial or final lattice vectors are returned.

        Returns:
            numpy.ndarray
        """
        ts.is_type((is_initial, bool, "is_initial"))
        rcp_latt = np.zeros(shape=(3, 3))
        if is_initial:
            rcp_raw = self._data.findall('structure')[0].find('crystal').findall('varray')[1]
        else:
            rcp_raw = self._data.findall('structure')[1].find('crystal').findall('varray')[1]
        for i in range(3):
            for j in range(3):
                rcp_latt[i, j] = float(rcp_raw[i].text.split()[j])
        return rcp_latt
