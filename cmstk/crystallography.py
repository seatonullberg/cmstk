from cmstk.utils import Number
import copy
import numpy as np
from typing import Any, Generator, List, MutableSequence, Optional, Sequence

try:
    import ase
except ImportError:
    has_ase = False
else:
    has_ase = True


class Atom(object):
    """Representation of an atom.

    Notes:
        One or both of `position_cartesian` and `position_direct` must be
        supplied as an argument.
        A 'direct' coordinate system is one in which the positions are 
        normalized by the lengths of their axes such that the largest magnitude
        in any direction is 1. 
        A 'cartesian' coordinate system is one in which the positions are not 
        normalized by the underlying axes.

    Args:
        charge: Electronic charge.
        magnetic_moment: Magnetic moment vector.
        position_cartesian: Atomic position in cartesian coordinates.
        position_direct: Atomic position in direct coordinates.
        symbol: IUPAC chemical symbol.
        velocity: Velocity vector.
    
    Attributes:
        charge: Electronic charge.
        magnetic_moment: Magnetic moment vector.
        position_cartesian: Atomic position in cartesian coordinates.
        position_direct: Atomic position in direct coordinates.
        symbol: IUPAC chemical symbol.
        velocity: Velocity vector.
    """

    def __init__(self, charge: Optional[Number] = None,
                 magnetic_moment: Optional[np.ndarray] = None,
                 position_cartesian: Optional[np.ndarray] = None,
                 position_direct: Optional[np.ndarray] = None,
                 symbol: Optional[str] = None,
                 velocity: Optional[np.ndarray] = None) -> None:
        if position_cartesian is None and position_direct is None:
            err = ("one or both of `position_cartesian` and `position_direct`\
                    must be populated.")
            raise ValueError(err)
        if charge is None:
            charge = 0
        self.charge = charge
        if magnetic_moment is None:
            magnetic_moment = np.array([])
        self.magnetic_moment = magnetic_moment
        if position_cartesian is None:
            position_cartesian = np.array([])
        self.position_cartesian = position_cartesian
        if position_direct is None:
            position_direct = np.array([])
        self.position_direct = position_direct
        if symbol is None:
            symbol = ""
        self.symbol = symbol
        if velocity is None:
            velocity = np.array([])
        self.velocity = velocity

    

class Lattice(object):
    """Representation of a crystal lattice.
    
    Args:
        angles: Tilt of each axis.
        atoms: Underlying collection of atoms.
        axes: Vectors defining the coordinate system.
        parameters: Scaling factor of each axis.

    Attributes:
        angles: Tilt of each axis.

    Properties:
        atoms: Underlying collection of atoms.
        axes: Vectors defining the coordinate system.
        charges: Charge of each atom.
        magnetic_moments: Magnetic moment of each atom.
        n_atoms: Total number of atoms in the lattice.
        parameters: Scaling factor of each axis.
        positions_cartesian: Position of each atom in cartesian coordinates.
        positions_direct: Position of each atom in direct coordinates.
        symbols: IUPAC chemical symbol of each atom.
        velocities: Velocity of each atom.
    """

    def __init__(self, angles: Optional[np.ndarray] = None,
                 atoms: Optional[MutableSequence[Atom]] = None,
                 axes: Optional[np.ndarray] = None,
                 parameters: Optional[np.ndarray] = None) -> None:
        if angles is None:
            angles = np.array([90, 90, 90])
        self.angles = angles
        if axes is None:
            axes = np.identity(3)
        self._axes = axes
        if parameters is None:
            parameters = np.array([1, 1, 1])
        self._parameters = parameters
        if atoms is None:
            atoms = []
        self._atoms = self._set_positions(atoms)

    @classmethod
    def from_ase(cls, ase_atoms: ase.Atoms, 
                 angles: Optional[np.ndarray] = None, 
                 axes: Optional[np.ndarray] = None,
                 parameters: Optional[np.ndarray] = None) -> Any:
        """Initializes a Lattice object from an ase.Atoms object.
        
        Notes:
            Only the cartesian positions are read in. In order to ensure proper
            scaling to direct coordinates, provide arguments for `axes` and 
            `parameters` function parameters.

        Args:
            ase_atoms: The ase.Atoms object to convert.
            angles: Tilt of each axis.
            axes: Vectors defining the coordinate system.
            parameters: Scaling factor of each axis.

        Returns:
            Lattice

        Raises:
            ImportError
            - If ase is not installed
        """
        if not has_ase:
            err = "this functionality requires the ase package"
            raise ImportError(err)
        quantities = {
            "charge": ase_atoms.get_initial_charges(),
            "magnetic_moment": ase_atoms.get_initial_magnetic_moments(),
            "position_cartesian": ase_atoms.get_positions(),
            "symbol": ase_atoms.get_chemical_symbols(),
            "velocity": ase_atoms.get_velocities()
        }
        # for whatever reason get_velocities() returns None inplace of an empty
        # array like the rest of them so I have to do this little hack right 
        # here to check for it and prevent errors in the dict comprehension
        if quantities["velocity"] is None:
            quantities["velocity"] = np.array([])
        lattice = cls(angles=angles, axes=axes, parameters=parameters)
        # iterate over each quantity individually in case it is empty
        for i in range(len(ase_atoms)):
            quantity = {
                k: (v[i] if i < len(v) else None) for k, v in quantities.items()
            }
            lattice.add_atom(Atom(**quantity))
        return lattice

    def add_atom(self, atom: Atom, 
                 tolerance: Optional[float] = None) -> None:
        """Adds an atom to the lattice if the position is not occupied.

        Notes:
            The tolerance distance is always calculated in direct coordinates
            so that the default value translates well across systems of 
            varying size.
        
        Args:
            atom: The atom the be added.
            tolerance: The radius in which to check for existing atoms.

        Returns:
            None

        Raises:
            ValueError
            - If an atom exists within the tolerance radius.
        """
        if tolerance is None:
            tolerance = 0.001
        atom = self._set_positions([atom])[0]
        for a in self.atoms:
            new = atom.position_direct
            existing = a.position_direct
            dist = np.sum(np.sqrt((new - existing)**2))
            if dist < tolerance:
                err = "an atom exists within the tolerance radius."
                raise ValueError(err)
        self._atoms.append(atom)

    def remove_atom(self, position: np.ndarray,
                    direct: Optional[bool] = None,
                    tolerance: Optional[float] = None) -> Atom:
        """Removes an atom from the lattice if the position is occupied.
        
        Args:
            position: The position to remove an atom from.
            direct: Specifies the use of direct coordinates.
            tolerance: The radius in which to check for existing atoms.

        Returns:
            A copy of the removed Atom object

        Raises:
            ValueError:
            - If no atom exists within the tolerance radius.
        """
        if direct is None:
            direct = True
        if tolerance is None:
            tolerance = 0.001
        removal_index = None
        removed_atom: Atom
        for i, a in enumerate(self.atoms):
            if direct:
                existing = a.position_direct
            else:
                existing = a.position_cartesian
            dist = np.sum(np.sqrt((position - existing)**2))
            if dist < tolerance:
                removal_index = i
                removed_atom = copy.deepcopy(a)
                break
        if removal_index is None:
            err = "an atom does not exist within the tolerance radius."
            raise ValueError(err)
        del self._atoms[removal_index]
        return removed_atom

    def group_atoms_by_symbol(self, order: Sequence[str]) -> None:
        """Groups atoms by their IUPAC chemical symbol.
        
        Notes:
            This operation alters the order of `self._atoms`.
        
        Args:
            order: IUPAC chemical symbols ordered in the way that the grouped 
            atoms will be ordered. 

        Returns:
            None
        
        Raises:
            ValueError:
            - If `order` is not a unique sequence.
            - If a member of order is not the symbol of any atom.
        """
        if len(order) != len(set(order)):
            err = "all members of `order` must be unique"
            raise ValueError(err)
        new = []
        for symbol in order:
            ok = False
            for a in self.atoms:
                if symbol == a.symbol:
                    new.append(a)
                    ok = True
            if not ok:
                err = "unrecognized symbol: {}".format(symbol)
                raise ValueError(err)
        self._atoms = new

    @property
    def atoms(self) -> Generator[Atom, None, None]: 
        for a in self._atoms:
            yield a

    @atoms.setter
    def atoms(self, value: MutableSequence[Atom]) -> None:
        self._atoms = self._set_positions(value)

    @property
    def axes(self) -> np.ndarray:
        return self._axes

    @axes.setter
    def axes(self, value: np.ndarray) -> None:
        # when axes are updated atomic positions must also be updated
        self._axes = value
        for a in self.atoms:
            a.position_cartesian = np.array([])
        self._atoms = self._set_positions(self._atoms)

    @property
    def charges(self) -> np.ndarray:
        return np.array([a.charge for a in self.atoms])

    @property
    def magnetic_moments(self) -> np.ndarray:
        return np.array([a.magnetic_moment for a in self.atoms])

    @property
    def n_atoms(self) -> int:
        return len(self._atoms)

    @property
    def parameters(self) -> np.ndarray:
        return self._parameters

    @parameters.setter
    def parameters(self, value: np.ndarray) -> None:
        # when parameters are updated atomic positions must also be updated
        self._parameters = value
        for a in self.atoms:
            a.position_cartesian = np.array([])
        self._atoms = self._set_positions(self._atoms)

    @property
    def positions_cartesian(self) -> np.ndarray:
        return np.array([a.position_cartesian for a in self.atoms])

    @property
    def positions_direct(self) -> np.ndarray:
        return np.array([a.position_direct for a in self.atoms])

    @property
    def symbols(self) -> List[str]:
        return [a.symbol for a in self.atoms]

    @property
    def velocities(self) -> np.ndarray:
        return np.array([a.velocity for a in self.atoms])

    def _set_positions(self, atoms: MutableSequence[Atom]) ->\
        MutableSequence[Atom]:
        """Sets position of each atom in cartesian and direct systems.
        
        Notes:
            This strategy is valid becuase the user is required to define at 
            least one of the position types. Therefore, using either the user 
            supplied or default lattice parameters and axes, conversion between
            cartesian and direct can be done with simple multiplication or 
            division of a conversion factor. 

        Args:
            atoms: The atoms to modify.

        Returns:
            The modified atoms.
        """
        factor = np.diag(self.parameters * self.axes)
        for a in atoms:
            # multiply by the factor for cartesian
            if a.position_cartesian.size == 0:
                a.position_cartesian = (a.position_direct * factor).flatten()
            # divide by the factor for direct
            if a.position_direct.size == 0:
                a.position_direct = (a.position_cartesian / factor).flatten()
        return atoms
