from typing import Optional, Sequence


class OszicarFile(object):
    """File wrapper from a VASP OSZICAR file.

    Notes:
        This is a read-only file wrapper.
        This wrapper is not robust to a wide range of IBRION values.
        TODO:
        - Future updates must check keyword rather than order.

    Args:
        filepath (optional) (str): Filepath to an OSZICAR file.
        total_free_energy (sequence of float): Total free energy at each ionic 
        step.
        e0 (sequence of float): Energy where sigma == 0 at each ionic step.
        delta_energy (sequence of float): Change in total energy at each ionic 
        step.
        magnetization (sequence of float): Magnetization at each ionic step.
     """

    def __init__(self, filepath: str = "OSZICAR") -> None:
        self.filepath = filepath
        self.total_free_energy: Sequence[float]
        self.e0: Sequence[float]
        self.delta_energy: Sequence[float]
        self.magnetization: Sequence[float]

    def read(self, path: Optional[str] = None) -> None:
        """Reads an OSZICAR file.
        
        Args:
            path (optional) (str): The filepath to read from.

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
            l = line.split()
            total_free_energy_values.append(float(l[2]))
            e0_values.append(float(l[4]))
            delta_energy_values.append(float(l[7].replace("=", "")))
            magnetization_values.append(float(l[9]))
        self.total_free_energy = tuple(total_free_energy_values)
        self.e0 = tuple(e0_values)
        self.delta_energy = tuple(delta_energy_values)
        self.magnetization = tuple(magnetization_values)
