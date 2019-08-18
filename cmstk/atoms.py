from cmstk.utils import Number
import copy
import numpy as np
from typing import Any, Generator, List, MutableSequence, Optional, Sequence


class Atom(object):
    """Representation of an Atom.
    
    Args:
        charge: Electronic charge.
        magnetic_moment: Magnetic moment vector.
        position: Position in space.
        symbol: IUPAC chemical symbol.
        velocity: Velocity vector.

    Attributes:
        charge: Electronic charge.
        magnetic_moment: Magnetic moment vector.
        position: Position in space.
        symbol: IUPAC chemical symbol.
        velocity: Velocity vector.
    """

    def __init__(self, charge: Optional[Number] = None,
                 magnetic_moment: Optional[np.ndarray] = None,
                 position: Optional[np.ndarray] = None,
                 symbol: Optional[str] = None,
                 velocity: Optional[np.ndarray] = None) -> None:
        if charge is None:
            charge = 0
        self.charge = charge
        if magnetic_moment is None:
            magnetic_moment = np.array([])
        self.magnetic_moment = magnetic_moment
        if position is None:
            position = np.array([])
        self.position = position
        if symbol is None:
            symbol = ""
        self.symbol = symbol
        if velocity is None:
            velocity = np.array([])
        self.velocity = velocity


class AtomCollection(object):
    """A generic collection of atoms.
    
    Args:
        atoms: The atoms in the collection.

    Attributes:
        atoms: The atoms in the collection.
        charges: Electronic charge of each atom.
        magnetic_moments: Magnetic moment vector of each atom.
        n_atoms: Number of atoms in the collection.
        positions: Position in space of each atom.
        symbols: IUPAC chemical symbol of each atom.
        velocities: Velocity vector of each atom.
    """

    def __init__(self, atoms: Optional[MutableSequence[Atom]] = None) -> None:
        if atoms is None:
            atoms = []
        self._atoms = atoms

    def add_atom(self, atom: Atom, tolerance: Optional[float] = None) -> None:
        """Adds an atom to the collection if its position is not occupied.

        Args:
            atom: The atom to be added.
            tolerance: The radius in which to check for existing atoms.

        Raises:
            ValueError
            - An atom exists within the tolerance radius.
        """
        if tolerance is None:
            tolerance = 0.001
        for a in self.atoms:
            new_position = atom.position
            existing_position = a.position
            distance = np.sum(np.sqrt((new_position - existing_position)**2))
            if distance < tolerance:
                err = "An atom exists within the tolerance radius ({}).".format(
                    tolerance
                )
                raise ValueError(err)
        self._atoms.append(atom)

    def remove_atom(self, position: np.ndarray, 
                    tolerance: Optional[float] = None) -> Atom:
        """Removes an atom from the collection if the position is occupied and 
           returns it
        
        Args:
            position: The position to remove an atom from.
            tolerance: The raidus in which to check for existing atoms.

        Raises:
            ValueError:
                There are no atoms in the collection.
                No atoms exist within the tolerance radius.
        """
        if tolerance is None:
            tolerance = 0.001
        if self.n_atoms == 0:
            err = "There are no atoms in the collection."
            raise ValueError(err)
        removal_index = None
        for i, a in enumerate(self.atoms):
            distance = np.sum(np.sqrt((position - a.position)**2))
            if distance < tolerance:
                removal_index = i
                break
        if removal_index is None:
            err = "No atoms exist within the tolerance radius ({}).".format(
                tolerance
            )
            raise ValueError(err)
        removed_atom = copy.deepcopy(self._atoms[removal_index])
        del self._atoms[removal_index]
        return removed_atom

    def sort_by_charge(self, hl: Optional[bool] = None) -> None:
        """Groups atoms by their electronic charges.
        
        Args:
            hl: Flag indicating high-to-low ordering.
        """
        if hl is None:
            hl = False
        self._atoms.sort(key=lambda x: x.charge, reverse=hl)

    def sort_by_magnetic_moment(self, hl: Optional[bool] = None) -> None:
        """Groups atoms by the magnitudes of their magnetic moments.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        if hl is None:
            hl = False
        self._atoms.sort(key=lambda x: np.linalg.norm(x.magnetic_moment), 
                         reverse=hl)

    def sort_by_position(self, hl: Optional[bool] = None) -> None:
        """Groups atoms by the magnitudes of their positions.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        if hl is None:
            hl = False
        self._atoms.sort(key=lambda x: x.linalg.norm(x.position), reverse=hl)

    def sort_by_symbol(self, order: Sequence[str]) -> None:
        """Groups atoms by their IUPAC chemical symbols in the given order.
        
        Args:
            order: IUPAC chemical symbols in a desired sequence.

        Raises:
            ValueError:
            - `order` must be a unique sequence.
            - A symbol in the collection is not found in `order`.
            - A symbol in `order` is not found in the collection.
            
        """
        if len(order) != len(set(order)):
            err = "`order` must be a unique sequence."
            raise ValueError(err)
        for symbol in self.symbols:
            if symbol not in order:
                err = "A symbol in the collection is not found in `order` ({})."
                .format(symbol)
                raise ValueError(err)
        atoms = []
        for symbol in order:
            ok = False
            for a in self.atoms:
                if symbol == a.symbol:
                    atoms.append(a)
                    ok = True
            if not ok:
                err = "A symbol in `order` is not found in the collection ({})."
                .format(symbol)
                raise ValueError(err)
        self._atoms = atoms

    def sort_by_velocity(self, hl: Optional[bool] = None) -> None:
        """Groups atoms by the magnitudes of their velocities.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        if hl is None:
            hl = False
        self._atoms.sort(key=lambda x: np.linalg.norm(x.velocity), reverse=hl)

    @property
    def atoms(self) -> Generator[Atom, None, None]:
        for a in self._atoms:
            yield a

    @property
    def charges(self) -> Generator[float, None, None]:
        for a in self._atoms:
            yield a.charge

    @property
    def magnetic_moments(self) -> Generator[np.ndarray, None, None]:
        for a in self._atoms:
            yield a.magnetic_moment

    @property
    def n_atoms(self) -> int:
        return len(self._atoms)

    @property
    def positions(self) -> Generator[np.ndarray, None, None]:
        for a in self._atoms:
            yield a.position

    @property
    def symbols(self) -> Generator[str, None, None]:
        for a in self._atoms:
            yield a.symbol
    
    @property
    def velocities(self) -> Generator[np.ndarray, None, None]:
        for a in self._atoms:
            yield a.velocity


class Lattice(AtomCollection):
    """Representation of a collection of atoms ordered in a crystalline 
       structure.
    
    Args:
        atoms: The atoms in the collection.
        vacuum: The thickness of the vacuum layer.

    Attributes:
        angles: Defining angles of the lattice (alpha, beta, gamma).
        atoms: The atoms in the collection.
        charges: Electronic charge of each atom.
        fractional_positions: Positions in space of each atom scaled to the 
                              lattice.
        magnetic_moments: Magnetic moment vector of each atom.
        n_atoms: Number of atoms in the collection.
        parameters: Defining dimensions of the lattice (a, b, c).
        positions: Position in space of each atom.
        symbols: IUPAC chemical symbol of each atom.
        vacuum: The thickness of the vacuum layer.
        velocities: Velocity vector of each atom.
    """

    def __init__(self, atoms: Optional[MutableSequence[Atom]] = None,
                 vacuum: Optional[Number] = None) -> None:
        if vacuum is None:
            vacuum = 0
        self.vacuum = vacuum
        super().__init__(atoms)

    @property
    def angles(self) -> np.ndarray:
        raise NotImplementedError

    @angles.setter
    def angles(self, value: np.ndarray) -> None:
        raise NotImplementedError

    @property
    def fractional_positions(self) -> Generator[np.ndarray, None, None]:
        raise NotImplementedError

    @property
    def parameters(self) -> np.ndarray:
        raise NotImplementedError

    @parameters.setter
    def parameters(self, value: np.ndarray) -> None:
        raise NotImplementedError
