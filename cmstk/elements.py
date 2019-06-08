import os
import json


class Database(object):
    """A read-only collection of elemental data.
    
    Args:
        filepath (optional) (str): Filepath to a json database.
    """

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = os.path.abspath(__file__)
            filepath = os.path.dirname(filepath)
            filepath = os.path.dirname(filepath)
            filepath = os.path.join(filepath, "data", "elements.json")
        assert type(filepath) is str
        self._filepath = filepath
        with open(filepath, "r") as f:
            self._data = json.load(f)

    def atomic_number(self, symbol):
        """Returns the atomic number of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_number"]

    def atomic_radius(self, symbol):
        """Returns the atomic radius of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_radius"]

    def atomic_weight(self, symbol):
        """Returns the atomic weight of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_weight"]

    def covalent_radius(self, symbol):
        """Returns the covalent radius of an IUPAC chemical symbol."""
        return self._data[symbol]["covalent_radius"]

    def lattice_constants(self, symbol, structure):
        """Returns the lattice constants of an IUPAC chemical symbol for a 
        particular lattice structure."""
        return self._data[symbol]["lattice_constants"][structure]

    def read(self, path=None):
        """Reads a json database.
        
        Args:
            path (optional) (str): Filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        assert type(path) is str
        with open(path, "r") as f:
            self._data = json.load(f)

    def write(self, path=None):
        """Writes a json database.
        
        Args:
            path (optional) (str): Filepath to write to.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        assert type(path) is str
        with open(path, "w") as f:
            json.dump(self._data)

    @property
    def filepath(self):
        """(str): Returns the path to a json database."""
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        if type(value) is not str:
            raise TypeError()
        self._filepath = value
