import math
from cmstk.data import ElementsReader
from cmstk.lattice.exceptions import AtomicPositionError
from cmstk.units.distance import DistanceUnit, Picometer


def separation_distance(p1, p2):
    """Returns the separation distance between two positions.

    Args:
        p1 (AtomicPosition): The first position.
        p2 (AtomicPosition): the second position.

    Returns:
        Picometer
    """
    pico_x1, pico_x2 = p1[0].to(Picometer), p2[0].to(Picometer)
    pico_y1, pico_y2 = p1[1].to(Picometer), p2[1].to(Picometer)
    pico_z1, pico_z2 = p1[2].to(Picometer), p2[2].to(Picometer)
    # use .value because squaring would throw conversion error
    distance = math.sqrt((pico_x1-pico_x2).value**2 + (pico_y1-pico_y2).value**2 + (pico_z1-pico_z2).value**2)
    return Picometer(distance)


class AtomicPosition(object):
    """Representation of 3D coordinates.

    Notes:
        Overrides __getitem__ and __setitem__ to access underlying position value directly.
        Provides a means of data integrity without constant manual verification.
    
    Args:
        position (tuple of DistanceUnit): (x, y, z) spatial coordinates 
    """

    def __init__(self, position):
        if type(position) is not tuple:
            raise TypeError("`position` must be of type tuple")
        for p in position:
            if not isinstance(p, DistanceUnit):
                raise TypeError("all members of `position` must be an instance of type DistanceUnit")
        if len(position) != 3:
            raise ValueError("`position` must have length 3")
        
        self._position = position

    def __iter__(self):
        return self._position.__iter__()

    def __getitem__(self, key):
        return self._position.__getitem__(key)

    def __setitem__(self, key, value):
        if not isinstance(value, DistanceUnit):
            raise TypeError("AtomicPosition only accepts instances of type DistanceUnit")
        return self._position.__setitem__(key, value)


class Atom(object):
    """Representation of an atom in space.
    
    Args:
        symbol (str): IUPAC chemical symbol.
        position (AtomicPosition): Verified (x, y, z) spatial coordinates.

    Attributes:
        symbol (str): IUPAC chemical symbol.
        position (AtomicPosition): Verified (x, y, z) spatial coordinates.
    """

    def __init__(self, symbol, position):
        if type(symbol) is not str:
            raise TypeError("`symbol` must be of type str")
        self.symbol = symbol

        if type(position) is not AtomicPosition:
            raise TypeError("`position` must be of type AtomicPosition")
        self.position = position

        self._elements_reader = ElementsReader() # store this for easy access in properties

    @property
    def atomic_radius(self):
        """Returns the Atom's radius as described in elements.json.
        
        Returns:
            Picometer
        """
        return self._elements_reader.atomic_radius(self.symbol)

    @property
    def crystal_structure(self):
        """Returns the Atom's crystal structure as described in elements.json.
        
        Returns:
            str
        """
        return self._elements_reader.crystal_structure(self.symbol)

    @property
    def lattice_constants(self):
        """Returns the Atom's lattice constants as described in elements.json.
        
        Returns:
            tuple of Picometer
        """
        return self._elements_reader.lattice_constants(self.symbol)


class Lattice(object):
    """Representation of a crystalline lattice.

    Args:
        atoms (list of Atom): Collection of atoms in the lattice.
    """

    def __init__(self, atoms=None):
        if atoms is None:
            atoms = []
        if type(atoms) is not list:
            raise TypeError("`atoms` must be of type list")
        for a in atoms:
            if type(a) is not Atom:
                raise TypeError("all members of list `atoms` must be of type Atom")

        self._atoms = atoms

    @property
    def atoms(self):
        """Returns a generator of all atoms."""
        for a in self._atoms:
            yield a

    @property
    def n_atoms(self):
        """Returns the number of atoms."""
        return len(self._atoms)

    def add_atom(self, atom):
        """Adds an atom to the lattice if the position is not already occupied.

        Args:
            atom (Atom): The atom to add.
        
        Raises:
            AtomicPositionError - If an atom already exists in the given position.
        """
        if type(atom) is not Atom:
            raise TypeError("`atom` must be of type Atom")

        for a in self.atoms:
            minimum_separation = a.atomic_radius + atom.atomic_radius
            actual_separation = separation_distance(a.position, atom.position)
            if actual_separation < minimum_separation:
                raise AtomicPositionError(position=atom.position, exists=True)
        self._atoms.append(atom)

    def remove_atom(self, position):
        """Removes an atom if the position is occupied.
        
        Args:
            position (AtomicPosition): Verified (x, y, z) spatial coordinates.
        
        Raises:
            AtomicPositionError - If an atom does not exist in the given position.
        """
        if type(position) is not AtomicPosition:
            raise TypeError("`position` must be of type AtomicPosition")

        for i, a in enumerate(self._atoms):  # iterate over the actual list because it may be modified intermediately
            separation = separation_distance(position, a.position)
            if separation < a.atomic_radius:
                del self._atoms[i]
                return
        raise AtomicPositionError(position=position, exists=False)

    @classmethod
    def from_file(cls, path, t):
        """Initializes a Lattice struct from a supported file type.
        
        Args:
            path (str): Path to the file.
            t (type): Type to interpret the file as
            - Must be a subclass of `BaseLatticeFile`
        """
        if type(path) is not str:
            raise TypeError("`path` must be of type str")
        if not issubclass(t, BaseLatticeFile):
            raise TypeError("`t` must be a subclass of type BaseLatticeFile")
        
        obj = t(path=path)
        atoms = obj.read()
        return cls(atoms=atoms)

    def to_file(self, path, t):
        """Writes a lattice to a supported file type.
        
        Args:
            path (str): File path to write the lattice to.
            t (type): The class representation of a supported file type
            - Must be a subclass of `BaseLatticeFile`
        """
        if type(path) is not str:
            raise TypeError("`path` must be of type str")
        if not issubclass(t, BaseLatticeFile):
            raise TypeError("`t` must be a subclass of type BaseLatticeFile")
        
        obj = t(path=path, lattice=self)
        obj.write()


class BaseLatticeFile(object):
    """Abstract representation of a file into which a lattice can be written."""