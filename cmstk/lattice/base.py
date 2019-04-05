

class Atom(object):
    """Representation of an atom in space.
    
    Args:
        symbol (str): IUPAC chemical symbol.
        position (tuple): (x, y, z) spatial coordinates.

    Attributes:
        symbol (str): IUPAC chemical symbol.
        position (tuple of float): (x, y, z) spatial coordinates.
    """

    def __init__(self, symbol, position):
        if type(symbol) is not str:
            raise TypeError("`symbol` must be of type str")
        self.symbol = symbol

        if type(position) is not tuple:
            raise TypeError("`position` must be of type tuple")
        if len(position) != 3:
            raise ValueError("`position` must have length 3")
        for p in position:
            if type(p) is not float:
                raise TypeError("all members of tuple `position` must be of type float")
        self.position = position


class Lattice(object):
    """Representation of a crystalline lattice.

    Args:
        atoms (list of Atom): Collection of atoms in the lattice.
    """

    def __init__(self, atoms):
        if type(atoms) is not list:
            raise TypeError("`atoms` must be of type list")
        for a in atoms:
            if type(a) is not Atom:
                raise TypeError("all members of list `atoms` must be of type Atom")
        self._atoms = atoms

    @classmethod
    def from_file(cls, path, t):
        """Initializes a Lattice struct from a supported file type.
        
        Args:
            path (str): Path to the file.
            t (type): Type to interpret the file as
            - Must be a subclass of `LatticeFile`
        """
        # TODO

    # TODO: not sure if this works
    @property
    def atoms(self):
        for a in self._atoms:
            yield a

    def add_atom(self, atom):
        """Adds an atom to the lattice if the position is not already occupied.

        Args:
            atom (Atom): The atom to add.
        
        Raises:
            AtomicPositionError - If an atom already exists in the given position.
        """
        if type(atom) is not Atom:
            raise TypeError("`atom` must be of type Atom")
        # TODO: check for availability of the space
        # use the atomic radii as the tolerance for addition
        self._atoms.append(atom)

    def remove_atom(self, position):
        """Removes an atom if position is within the radius of an existing atom.
        
        Args:
            position (tuple of float): (x, y, z) spatial coordinates.
        
        Raises:
            AtomicPositionError - If an atom does not exist in the given position.
        """
        if type(position) is not tuple:
            raise TypeError("`position` must be of type tuple")
        if len(position) != 3:
            raise ValueError("`position` must have length 3")
        for p in position:
            if type(p) is not float:
                raise TypeError("all members of tuple `position` must be of type float")
        
        # TODO: check for atom in this space and remove if exists
        # del self._atoms[index]

    def write(self, t):
        """Writes a lattice to a supported file type.
        
        Args:
            t (type): The class representation of a supported file type
            - Must be a subclass of `LatticeFile`
        """
        # TODO


class LatticeFile(object):
    """Representation of a file type which a lattice can be written into."""
        
