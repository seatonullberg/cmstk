import numpy as np
from typing import Iterable, Optional


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

    def __init__(self, atoms: Iterable[Atom], principal_axes: np.ndarray,
                 parameters: np.ndarray, angles: np.ndarray,
                 coordinate_system: str = "direct") -> None:
        self.atoms = atoms
        self.principal_axes = principal_axes
        self.parameters = parameters
        self.angles = angles
        self.coordinate_system = coordinate_system

    # TODO:
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
        raise NotImplementedError()

    # TODO:
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
        raise NotImplementedError()

    # TODO:
    def translate(self, translation: np.ndarray) -> None:
        """Translates the lattice by a 3D translation vector.
        
        Args:
            translation (numpy.ndarray): The translation vector.

        Returns:
            None
        
        Raises:
            ValueError
            - If the translation is not a 3D vector.
        """
        raise NotImplementedError()

    # TODO:
    def rotate(self, rotation: np.ndarray) -> None:
        """Rotates the lattice by a 3D rotation vector.
        
        Args:
            rotation (numpy.ndarray): The rotation vector.
        
        Returns:
            None

        Raises:
            ValueError
            - If the rotation is not a 3D vector.
        """
        raise NotImplementedError()

    # TODO:
    def repeat(self, size: np.ndarray) -> None:
        """Repeates the lattice in 3 dimensions.
        
        Args:
            size (numpy.ndarray): The number of repetitions in each direction.

        Returns:
            None

        Raises:
            ValueError
            - If the size is not a 3D vector.
        """
        raise NotImplementedError()

    # TODO:
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
        raise NotImplementedError()
