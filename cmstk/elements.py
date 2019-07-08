from cmstk.utils import data_directory
import json
import os
from typing import List, Optional


class Database(object):
    """A collection of elemental data.
    
    Args:
        filepath (optional) (str): Filepath to a json database.

    Attributes:
        filepath (optional) (str): Filepath to a json database.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = os.path.join(data_directory(), "elements.json")
        self.filepath = filepath
        with open(filepath, "r") as f:
            self._data = json.load(f)

    def atomic_number(self, symbol: str) -> int:
        """Returns the atomic number of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_number"]

    def atomic_radius(self, symbol: str) -> float:
        """Returns the atomic radius of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_radius"]

    def atomic_weight(self, symbol: str) -> float:
        """Returns the atomic weight of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_weight"]

    def covalent_radius(self, symbol: str) -> float:
        """Returns the covalent radius of an IUPAC chemical symbol."""
        return self._data[symbol]["covalent_radius"]

    def lattice_constants(self, symbol: str, structure: str) -> List[float]:
        """Returns the lattice constants of an IUPAC chemical symbol for a 
        particular lattice structure."""
        return self._data[symbol]["lattice_constants"][structure]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a json database.
        
        Args:
            path (optional) (str): Filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            self._data = json.load(f)

    def write(self, path: Optional[str] = None) -> None:
        """Writes a json database.
        
        Args:
            path (optional) (str): Filepath to write to.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            json.dump(self._data, f)
