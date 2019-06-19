from cmstk.base import BaseFile


class OszicarFile(BaseFile):
    """File wrapper from a VASP OSZICAR file.

    Notes:
        This is a read-only file wrapper.
        This wrapper is not robust to a wide range of IBRION values.
        TODO:
        - Future updates must check keyword rather than order.

    Args:
        filepath (optional) (str): Filepath to an OSZICAR file.
    """

    def __init__(self, filepath="OSZICAR"):
        super().__init__(filepath)
        self._total_free_energy = None
        self._e0 = None
        self._delta_energy = None
        self._magnetization = None

    def read(self, path=None):
        """Reads an OSZICAR file.
        
        Args:
            path (optional) (str): Filepath to read.

        Returns:
            None 
        """ 
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        total_free_energy_values = []
        e0_values = []
        delta_energy_values = []
        magnetization_values = []
        # only parse ionic step lines
        # - they always start with an int
        lines = [l for l in lines if l.strip()[0].isdigit()]
        for line in lines:
            line = line.split()
            total_free_energy_values.append(float(line[2]))
            e0_values.append(float(line[4]))
            delta_energy_values.append(float(line[7].replace("=", "")))
            magnetization_values.append(float(line[9]))
        self.total_free_energy = tuple(total_free_energy_values)
        self.e0 = tuple(e0_values)
        self.delta_energy = tuple(delta_energy_values)
        self.magnetization = tuple(magnetization_values)
        
    @property
    def total_free_energy(self):
        """(tuple of float): Total free energy at each ionic step."""
        return self._total_free_energy

    @total_free_energy.setter
    def total_free_energy(self, value):
        if type(value) is not tuple:
            raise TypeError()
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._total_free_energy = value

    @property
    def e0(self):
        """(tuple of float): Energy where sigma == 0 at each ionic step."""
        return self._e0

    @e0.setter
    def e0(self, value):
        if type(value) is not tuple:
            raise TypeError()
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._e0 = value

    @property
    def delta_energy(self):
        """(tuple of float): Change in total energy at each ionic step."""
        return self._delta_energy

    @delta_energy.setter
    def delta_energy(self, value):
        if type(value) is not tuple:
            raise TypeError()
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._delta_energy = value

    @property
    def magnetization(self):
        """(tuple of float): Magnetization at each ionic step."""
        return self._magnetization

    @magnetization.setter
    def magnetization(self, value):
        if type(value) is not tuple:
            raise TypeError()
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._magnetization = value


if __name__ == "__main__":
    path = "/home/seaton/python-repos/cmstk/data/vasp/OSZICAR"
    oszicar = OszicarFile(path)
    oszicar.read()