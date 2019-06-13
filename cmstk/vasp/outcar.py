from cmstk.base import BaseFile


class OutcarFile(BaseFile):
    """File wrapper for a VASP OUTCAR file.
    
    Notes:
        This is a read-only file wrapper.

    Args:
        filepath (optional) (str): Filepath to an OUTCAR file.
    """

    def __init__(self, filepath="OUTCAR"):
        super().__init__(filepath)
        self._entropy = None
        self._total_energy = None

    def read(self, path=None):
        """Reads an OUTCAR file.
        
        Args:
            path (optional) (str): Filepath to read.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        entropy_values = []
        total_energy_values = []
        for line in lines:
            split_line = line.split()
            if "EENTRO" in split_line:
                entropy_values.append(float(split_line[-1]))
            elif "TOTEN" in split_line:
                total_energy_values.append(float(split_line[-2]))  # skip `eV`
        self.entropy = tuple(entropy_values)
        self.total_energy = tuple(total_energy_values)

    @property
    def entropy(self):
        """(tuple of float): Entropy value of the system reported at each step 
        of the simulation."""
        return self._entropy
    
    @entropy.setter
    def entropy(self, value):
        if type(value) is not tuple:
            raise TypeError()
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._entropy = value

    @property
    def total_energy(self):
        """(tuple of float): Total (free energy) value of the system reported 
        at each step of the simulation."""
        return self._total_energy

    @total_energy.setter
    def total_energy(self, value):
        if type(value) is not tuple:
            raise TypeError()
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._total_energy = value

    