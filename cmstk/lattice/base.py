import math
from cmstk.data import ElementsReader
from cmstk.lattice.exceptions import AtomicPositionError
from cmstk.units.distance import DistanceUnit, Picometer
from cmstk.units.angle import AngleUnit, Radian
from cmstk.units.vector import Vector3D


def separation_distance(p1, p2):
    """Returns the separation distance between two positions.

    Args:
        p1 (Vector3D): The first position.
        p2 (Vector3D): the second position.

    Returns:
        Picometer
    """
    pico_x1, pico_x2 = p1[0].to(Picometer), p2[0].to(Picometer)
    pico_y1, pico_y2 = p1[1].to(Picometer), p2[1].to(Picometer)
    pico_z1, pico_z2 = p1[2].to(Picometer), p2[2].to(Picometer)
    # use .value because squaring would throw conversion error
    distance = math.sqrt((pico_x1-pico_x2).value**2 + (pico_y1-pico_y2).value**2 + (pico_z1-pico_z2).value**2)
    return Picometer(distance)


class Atom(object):
    """Representation of an atom in space.
    
    Args:
        symbol (str): IUPAC chemical symbol.
        position (Vector3D): Verified (x, y, z) spatial coordinates.

    Attributes:
        symbol (str): IUPAC chemical symbol.
        position (Vector3D): Verified (x, y, z) spatial coordinates.
    """

    def __init__(self, symbol, position):
        if type(symbol) is not str:
            raise TypeError("`symbol` must be of type str")
        self.symbol = symbol

        if type(position) is not Vector3D:
            raise TypeError("`position` must be of type Vector3D")
        if position.unit_kind is not DistanceUnit:
            raise TypeError("`position` must contain units of kind DistanceUnit")
        
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
    def covalent_radius(self):
        """Returns the Atom's covalent radius as described in elements.json.
        
        Returns:
            Picometer
        """
        return self._elements_reader.covalent_radius(self.symbol)

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

    ################
    #  Properties  #
    ################

    @property
    def atoms(self):
        """Returns a generator of all atoms."""
        for a in self._atoms:
            yield a

    @property
    def n_atoms(self):
        """Returns the number of atoms."""
        return len(self._atoms)

    #######################
    #  Atomic Operations  #
    #######################

    def add_atom(self, atom, tolerance=None):
        """Adds an atom to the lattice if the position is not already occupied.

        Args:
            atom (Atom): The atom to add.
            tolerance (optional) (DistanceUnit): Minimum separation distance for valid addition.
            - `tolerance` defaults to the covalent radius of `atom` plus that of its nearest neighbor.
        
        Raises:
            AtomicPositionError - If an atom already exists in the given position.
        """
        if type(atom) is not Atom:
            raise TypeError("`atom` must be of type Atom")
        if tolerance is not None:
            if not isinstance(tolerance, DistanceUnit):
                raise TypeError("`tolerance` must be an instance of DistanceUnit")

        for a in self.atoms:
            if tolerance is None:
                minimum_separation = a.covalent_radius + atom.covalent_radius
            else:
                minimum_separation = tolerance.to(Picometer)
            actual_separation = separation_distance(a.position, atom.position)
            if actual_separation < minimum_separation:
                raise AtomicPositionError(position=atom.position, exists=True)
        self._atoms.append(atom)

    def remove_atom(self, position, tolerance=None):
        """Removes an atom if the position is occupied.
        
        Args:
            position (Vector3D): Verified (x, y, z) spatial coordinates.
            tolerance (optional) (DistanceUnit): Maximum separation distance from another atomic center for valid removal.
            - `tolerance` defaults to the covalent radius of `atom`'s nearest neighbor.
        
        Raises:
            AtomicPositionError - If an atom does not exist in the given position.
        """
        if type(position) is not Vector3D:
            raise TypeError("`position` must be of type Vector3D")
        if position.unit_kind is not DistanceUnit:
            raise TypeError("`position` must contain units of kind DistanceUnit")
        if tolerance is not None:
            if not isinstance(tolerance, DistanceUnit):
                raise TypeError("`tolerance` must be an instance of DistanceUnit")

        for i, a in enumerate(self._atoms):  # iterate over the actual list because it may be modified intermediately
            if tolerance is None:
                maximum_separation = a.covalent_radius
            else:
                maximum_separation = tolerance.to(Picometer)

            separation = separation_distance(position, a.position)
            if separation < maximum_separation:
                del self._atoms[i]
                return
        raise AtomicPositionError(position=position, exists=False)

    # TODO
    ########################
    #  Lattice Operations  #
    ########################

    def repeat(self, dims):
        """Repeat the lattice in 3 dimensions.
    
        Args:
            dims (tuple of ints): The number of times to repeat in each direction (x, y, z).
        """
        if type(dims) is not tuple:
            raise TypeError("`dims` must be of type tuple")
        if len(dims) != 3:
            raise ValueError("`dims` must have length 3")
        for d in dims:
            if type(d) is not int:
                raise TypeError("all members of `dims` must be of type int")
        raise NotImplementedError

    def rotate(self, angles):
        """Rotate the lattice in 3 dimensions.

        Args:
            angles (Vector3D of AngleUnits): Angles to rotate the lattice by in (x, y, z).
        """
        if type(angles) is not Vector3D:
            raise TypeError("`angles` must be of type Vector3D")
        if angles.unit_kind is not AngleUnit:
            raise TypeError("`angles` must contain units of kind AngleUnits")
        for a in self.atoms:
            a.position.rotate(angles)

    def translate(self, dims):
        """Translate the lattice in 3 dimensions.

        Args:
            dims (Vector3D of DistanceUnit): The distance to translate the lattice by in (x, y, z).
            - Here the Vector3D functions not as a point in space but a translation factor to move all atoms by.
            - This prevents having to do the type checking on a tuple of DistanceUnits which is already handled by Vector3D.
        """
        if type(dims) is not Vector3D:
            raise TypeError("`dims` must be of type Vector3D")
        if dims.unit_kind is not DistanceUnit:
            raise TypeError("`position` must contain units of kind DistanceUnit")
        for a in self.atoms:
            a.position.translate(dims)
