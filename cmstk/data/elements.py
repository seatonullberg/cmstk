from cmstk.data.base import BaseDataReader
from cmstk.units.distance import Picometer

# TODO: (maybe) alter such that units are returned 
# - provide methods to access elemental properties and return the value wrapped in the proper unit


class ElementsReader(BaseDataReader):
    """Represents access the the elements.json file in the top level data directory."""

    def __init__(self):
        super().__init__(filename="elements.json")

    def atomic_radius(self, symbol):
        """Returns atomic radius of `symbol` in Picometer units.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        
        Returns:
            Picometer
        """
        r = self[symbol]["atomic_radius"]
        return Picometer(r)

    def crystal_structure(self, symbol):
        """Returns crystal structure of `symbol`.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        
        Returns:
            str
        """
        structure = self[symbol]["crystal_structure"]
        return structure

    def lattice_constants(self, symbol):
        """Returns lattice constants of `symbol` in Picometer units.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        
        Returns:
            list of Picometer
        """
        constants = self[symbol]["lattice_constants"]
        typed_constants = [Picometer(c) for c in constants]
        return typed_constants
