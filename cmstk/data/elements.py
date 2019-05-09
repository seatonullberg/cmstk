from cmstk.data.base import BaseDataReader
from cmstk.units.distance import Picometer
from cmstk.units.mass import AtomicMassUnit


class ElementsReader(BaseDataReader):
    """Represents access the the elements.json file in the top level data directory."""

    def __init__(self):
        super().__init__()
        self.read_json("elements.json")

    def atomic_number(self, symbol):
        """Returns the atomic number of `symbol` as an int.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        """
        n = self[symbol]["atomic_number"]
        return n

    def atomic_radius(self, symbol):
        """Returns atomic radius of `symbol` in Picometer units.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        
        Returns:
            Picometer
        """
        r = self[symbol]["atomic_radius"]
        return Picometer(r)

    def atomic_weight(self, symbol):
        """Returns the atomic weight of `symbol` in AtomicMassUnit units.
        
        Args:
            symbol (str): IUPAC chemical symbol.

        Returns:
            AtomicMassUnit
        """
        weight = self[symbol]["atomic_weight"]
        return AtomicMassUnit(weight)

    def covalent_radius(self, symbol):
        """Returns covalent radius of `symbol` in Picometer units.
        
        Args:
            symbol (str): IUPAC chemical symbol.

        Returns:
            Picometer
        """
        r = self[symbol]["covalent_radius"]
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
            tuple of Picometer
        """
        constants = self[symbol]["lattice_constants"]
        typed_constants = [Picometer(c) for c in constants]
        return tuple(typed_constants)
