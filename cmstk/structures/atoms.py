from cmstk.utils import Number
import copy
import numpy as np
from typing import Generator, List, Optional, Sequence


class Atom(object):
    """Representation of an Atom.
    
    Args:
        charge: Electronic charge.
        magnetic_moment: Magnetic moment scalar.
        position: Position in space.
        symbol: IUPAC chemical symbol.
        velocity: Velocity vector.

    Attributes:
        charge: Electronic charge.
        magnetic_moment: Magnetic moment scalar.
        position: Position in space.
        symbol: IUPAC chemical symbol.
        velocity: Velocity vector.
    """
    def __init__(self,
                 charge: Optional[Number] = None,
                 magnetic_moment: Optional[Number] = None,
                 position: Optional[np.ndarray] = None,
                 symbol: Optional[str] = None,
                 velocity: Optional[np.ndarray] = None) -> None:
        if charge is None:
            charge = 0
        self.charge = charge
        if magnetic_moment is None:
            magnetic_moment = 0
        self.magnetic_moment = magnetic_moment
        if position is None:
            position = np.array([0, 0, 0])
        self.position = position
        if symbol is None:
            symbol = ""
        self.symbol = symbol
        if velocity is None:
            velocity = np.array([0, 0, 0])
        self.velocity = velocity


class AtomCollection(object):
    """A generic collection of atoms.
    
    Args:
        atoms: The atoms in the collection.
        tolerance: The radius in which to check for atoms on add or remove.

    Attributes:
        atoms: The atoms in the collection.
        charges: Electronic charge of each atom.
        magnetic_moments: Magnetic moment of each atom.
        n_atoms: Number of atoms in the collection.
        n_symbols: Number of symbols in the collection.
        positions: Position in space of each atom.
        symbols: IUPAC chemical symbol of each atom.
        tolerance: The radius in which to check for atoms on add or remove.
        velocities: Velocity vector of each atom.
    """
    def __init__(self,
                 atoms: Optional[List[Atom]] = None,
                 tolerance: Optional[Number] = None) -> None:
        if tolerance is None:
            tolerance = 0
        self.tolerance = tolerance
        if atoms is None:
            atoms = []
        self._atoms: List[Atom] = []
        for a in atoms:
            self.add_atom(a)

    def add_atom(self, atom: Atom) -> None:
        """Adds an atom to the collection if its position is not occupied.

        Args:
            atom: The atom to be added.

        Raises:
            ValueError
            - An atom exists within the tolerance radius.
        """
        for a in self.atoms:
            distance = np.sum(np.sqrt((atom.position - a.position)**2))
            if distance < self.tolerance:
                err = "An atom exists within the tolerance radius ({}).".format(
                    self.tolerance)
                raise ValueError(err)
        self._atoms.append(atom)

    def remove_atom(self, position: np.ndarray) -> Atom:
        """Removes an atom from the collection if the position is occupied and 
           returns it
        
        Args:
            position: The position to remove an atom from.

        Raises:
            ValueError:
                There are no atoms in the collection.
                No atoms exist within the tolerance radius.
        """
        if self.n_atoms == 0:
            err = "There are no atoms in the collection."
            raise ValueError(err)
        removal_index = None
        for i, a in enumerate(self.atoms):
            existing_position = a.position
            distance = np.sum(np.sqrt((position - existing_position)**2))
            if distance < self.tolerance:
                removal_index = i
                break
        if removal_index is None:
            err = "No atoms exist within the tolerance radius ({}).".format(
                self.tolerance)
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
        """Groups atoms by their magnetic moments.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        if hl is None:
            hl = False
        self._atoms.sort(key=lambda x: x.magnetic_moment, reverse=hl)

    def sort_by_position(self, hl: Optional[bool] = None) -> None:
        """Groups atoms by the magnitude of their positions.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        if hl is None:
            hl = False
        self._atoms.sort(key=lambda x: np.linalg.norm(x.position), reverse=hl)

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
                err = ("A symbol in the collection is not found in `order`"
                       " ({}).".format(symbol))
                raise ValueError(err)
        atoms = []
        for symbol in order:
            ok = False
            for a in self.atoms:
                if symbol == a.symbol:
                    atoms.append(a)
                    ok = True
            if not ok:
                err = ("A symbol in `order` is not found in the collection"
                       " ({}).".format(symbol))
                raise ValueError(err)
        self._atoms = atoms

    def sort_by_velocity(self, hl: Optional[bool] = None) -> None:
        """Groups atoms by the magnitude of their velocities.
        
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
    def charges(self) -> Generator[Number, None, None]:
        for a in self._atoms:
            yield a.charge

    @property
    def magnetic_moments(self) -> Generator[Number, None, None]:
        for a in self._atoms:
            yield a.magnetic_moment

    @property
    def n_atoms(self) -> int:
        return len(self._atoms)

    @property
    def n_symbols(self) -> int:
        return len(set([s for s in self.symbols]))

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
