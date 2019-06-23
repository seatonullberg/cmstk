import numpy as np
from typing import Optional, MutableSequence, Sequence


class Atom(object):
    """Representation of an atom.
    
    Args:
        symbol (str): IUPAC chemical symbol.
        position (numpy.ndarray): Coordinates in 3D.
        charge (optional) (float): Electronic charge of the atom.
        magnetic_moment (optional) (numpy.ndarray): Magnetic moment in 3D.
        velocity (optional) (numpy.ndarray): Velocity in 3D.
    
    Attributes:
        symbol (str): IUPAC chemical symbol.
        position (numpy.ndarray): Coordinates in 3D.
        charge (float): Electronic charge of the atom.
        magnetic_moment (numpy.ndarray): Magnetic moment in 3D.
        velocity (numpy.ndarray): Velocity in 3D.
    """

    def __init__(self, symbol: str, position: np.ndarray,
                 charge: Optional[float] = None, 
                 magnetic_moment: Optional[np.ndarray] = None,
                 velocity: Optional[np.ndarray] = None) -> None:
        self.symbol = symbol
        self.position = position
        self.charge = charge
        self.magnetic_moment = magnetic_moment
        self.velocity = velocity


class Lattice(object):
    """Representation of a crystal lattice.
    
    Args:
        atoms (iterable of Atoms): All atoms in the lattice.
        principal_axes (numpy.ndarray): Vectors defining the lattice.
        parameters (numpy.ndarray): Lengths of each principal axis.
        angles (numpy.ndarray): Tilt of each principal axis.
        coordinate_system (optional) (str): Specify `cartesian` or `direct`.

    Attributes:
        atoms (iterable of Atoms): All atoms in the lattice.
        principal_axes (numpy.ndarray): Vectors defining the lattice.
        parameters (numpy.ndarray): Lengths of each principal axis.
        angles (numpy.ndarray): Tilt of each principal axis.
        coordinate_system (optional) (str): Specify `cartesian` or `direct`.
    """

    def __init__(self, atoms: MutableSequence[Atom], principal_axes: np.ndarray,
                 parameters: np.ndarray, angles: np.ndarray,
                 coordinate_system: str = "direct") -> None:
        self._atoms = atoms
        self.principal_axes = principal_axes
        self.parameters = parameters
        self.angles = angles
        self._coordinate_system = coordinate_system

    def add_atom(self, atom: Atom, tolerance: float = 0.001) -> None:
        """Adds an atom to the lattice if the position is not occupied.
        
        Args:
            atom (Atom): The atom to add to the lattice.
            tolerance (optional) (float): Tolerance used to determine if an atom
            exists at the specified position.

        Returns:
            None

        Raises:
            ValueError
            - If an atom exists within tolerance boundary.
        """
        new_pos = atom.position
        for a in self.atoms:
            diff = np.sqrt((new_pos - a.position)**2)
            for d in diff:
                if d < tolerance:
                    err = "an atom already exists within the tolerance distance"
                    raise ValueError(err)
        self._atoms.append(atom)

    def remove_atom(self, position: np.ndarray, 
                    tolerance: float = 0.001) -> None:
        """Removes an atom from the lattice if the position is occupied.
        
        Args:
            position (numpy.ndarray): Position to remove an atom from.
            tolerance (optional) (float): Tolerance used to determine is an atom
            exists at the specified position.
        
        Returns:
            None

        Raises:
            ValueError
            - If an atom does not exist within tolerance boundary.
        """
        removal_index = None
        for i, a in enumerate(self.atoms):
            diff = np.sqrt((position - a.position)**2)
            for d in diff:
                if d < tolerance:
                    removal_index = i
        if removal_index is None:
            err = "an atom does not exist within the tolerance distance"
            raise ValueError(err)
        else:
            del self._atoms[removal_index]

    def group_atoms_by_symbol(self, order: Sequence[str]) -> None:
        """Groups atoms by their IUPAC chemical symbol.
        
        Args:
            order (list of str): IUPAC chemical symbols in the order which 
            groups are to be arranged.

        Returns:
            None
        
        Raises:
            ValueError:
            - If `order` has non-unique members.
            - If a member of `order` is not the symbol of any atom.
        """
        if len(order) != len(set(order)):
            raise ValueError("`order` must have unique members")
        new_atoms = []
        for symbol in order:
            ok = False
            for a in self.atoms:
                if symbol == a.symbol:
                    new_atoms.append(a)
                    ok = True
            if not ok:
                err = "symbol `{}` not found in atoms".format(symbol)
                raise ValueError(err)
        self._atoms = new_atoms

    def change_coordinate_system(self, system: str) -> None:
        """Modifies the coordinate system by which all atoms in the lattice are 
        represented.
        
        Args:
            system (str): The coordinate system to switch to.

        Returns:
            None
        
        Raises:
            ValueError:
            - If the system name is unsupported.
        """
        if self.coordinate_system == system:
            return
        if system == "cartesian":
            self._change_coordinate_system_cartesian()
        elif system == "direct":
            self._change_coordinate_system_direct()
        else:
            err = "coordinate system must be one of: cartesian, direct"
            raise ValueError(err)

    @property
    def atoms(self):
        """(iterator of Atom): Yileds all atoms in the lattice.
        
        Notes:
            This exists to prevent being able to append directly into 
            `self.atoms`.
            - Ensures the tolerance check is always done upon addition.
        """
        for a in self._atoms:
            yield a

    @atoms.setter
    def atoms(self, value: MutableSequence[Atom]):
        self._atoms = value

    @property
    def coordinate_system(self):
        """(str): Returns the coordinate system which all positions are in.

        Notes:
            No setter provided because that is always done internally. 
        """
        return self._coordinate_system

    def _change_coordinate_system_cartesian(self):
        factor = np.diag(self.parameters * self.principal_axes)
        for a in self.atoms:
            a.position = (a.position * factor).flatten()
        self._coordinate_system = "cartesian"

    def _change_coordinate_system_direct(self):
        factor = np.diag(self.parameters * self.principal_axes)
        for a in self.atoms:
            a.position = (a.position / factor).flatten()
        self._coordinate_system = "direct"
