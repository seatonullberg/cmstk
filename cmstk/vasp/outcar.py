from typing import Optional, Sequence


class OutcarFile(object):
    """File wrapper for a VASP OUTCAR file.
    
    Notes:
        This is a read-only file wrapper.

    Args:
        filepath (optional) (str): Filepath to an OUTCAR file.
        entropy (sequence of float): Entropy value of the system at each step.
        total_energy (sequence of float): Total (free energy) value of the 
        system at each step.
    """

    def __init__(self, filepath: str = "OUTCAR") -> None:
        self.filepath = filepath
        self.entropy: Sequence[float]
        self.total_energy: Sequence[float]

    def read(self, path: Optional[str] = None) -> None:
        """Reads an OUTCAR file.
        
        Args:
            path (optional) (str): The filepath to read from.

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
