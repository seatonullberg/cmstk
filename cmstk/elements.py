class Database(object):
    """A read-only collection of elemental data.
    
    Args:
        None
    """

    def __init__(self):
        pass

    def atomic_number(self, symbol):
        """Returns the atomic number of an IUPAC chemical symbol."""
        return self._data()[symbol]["atomic_number"]

    def atomic_radius(self, symbol):
        """Returns the atomic radius of an IUPAC chemical symbol."""
        return self._data()[symbol]["atomic_radius"]

    def atomic_weight(self, symbol):
        """Returns the atomic weight of an IUPAC chemical symbol."""
        return self._data()[symbol]["atomic_weight"]

    def covalent_radius(self):
        """Returns the covalent radius of an IUPAC chemical symbol."""
        return self._data()[symbol]["covalent_radius"]

    def lattice_constants(self, symbol, structure):
        """Returns the lattice constants of an IUPAC chemical symbol for a 
        particular lattice structure."""
        return self._data(symbol)["lattice_constants"][structure]

    def _data(self):
        return {}