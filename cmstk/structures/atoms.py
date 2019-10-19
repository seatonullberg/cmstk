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
                 charge: float = 0,
                 magnetic_moment: float = 0,
                 position: Optional[np.ndarray] = None,
                 symbol: str = "",
                 velocity: Optional[np.ndarray] = None) -> None:
        self.charge = charge
        self.magnetic_moment = magnetic_moment
        self.symbol = symbol
        if position is None:
            position = np.array([0, 0, 0])
        self.position = position
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
                 tolerance: float = 0.001) -> None:
        self.tolerance = tolerance
        if atoms is None:
            atoms = []
        self._atoms: List[Atom] = []
        self.atoms = atoms

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

    def sort_by_charge(self, hl: bool = False) -> None:
        """Groups atoms by their electronic charges.
        
        Args:
            hl: Flag indicating high-to-low ordering.
        """
        self._atoms.sort(key=lambda x: x.charge, reverse=hl)

    def sort_by_magnetic_moment(self, hl: bool = False) -> None:
        """Groups atoms by their magnetic moments.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        self._atoms.sort(key=lambda x: x.magnetic_moment, reverse=hl)

    def sort_by_position(self, hl: bool = False) -> None:
        """Groups atoms by the magnitude of their positions.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        self._atoms.sort(key=lambda x: np.linalg.norm(x.position), reverse=hl)

    def sort_by_symbol(self, order: List[str]) -> None:
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

    def sort_by_velocity(self, hl: bool = False) -> None:
        """Groups atoms by the magnitude of their velocities.
        
        Args:
            hl: Flag indicate high-to-low ordering.
        """
        self._atoms.sort(key=lambda x: np.linalg.norm(x.velocity), reverse=hl)

    def translate(self, translation: np.ndarray) -> None:
        """Translates all atoms in the collection by the `translation` vector.

        Args:
            translation: Translation vector.
        """
        atoms = []
        for a in self.atoms:
            a.position += translation
            atoms.append(a)
        self.atoms = atoms

    @property
    def atoms(self) -> List[Atom]:
        return copy.deepcopy(self._atoms)

    @atoms.setter
    def atoms(self, value: List[Atom]) -> None:
        self._atoms = []
        for a in value:
            self.add_atom(a)

    @property
    def charges(self) -> List[float]:
        return [a.charge for a in self._atoms]

    @charges.setter
    def charges(self, value: List[float]) -> None:
        if len(value) != len(self._atoms):
            err = "Number of charges must match number of atoms."
            raise ValueError(err)
        atoms = []
        for a, c in zip(self._atoms, value):
            a.charge = c
            atoms.append(a)
        self._atoms = atoms

    @property
    def magnetic_moments(self) -> List[float]:
        return [a.magnetic_moment for a in self._atoms]

    @magnetic_moments.setter
    def magnetic_moments(self, value: List[float]) -> None:
        if len(value) != len(self._atoms):
            err = "Number of magnetic_moments must match number of atoms."
            raise ValueError(err)
        atoms = []
        for a, mm in zip(self._atoms, value):
            a.magnetic_moment = mm
            atoms.append(a)
        self._atoms = atoms

    @property
    def n_atoms(self) -> int:
        return len(self._atoms)

    @property
    def n_symbols(self) -> int:
        return len(set([s for s in self.symbols]))

    @property
    def positions(self) -> List[np.ndarray]:
        return [a.position for a in self._atoms]

    @positions.setter
    def positions(self, value: List[np.ndarray]):
        if len(value) != len(self._atoms):
            err = "Number of positions must match number of atoms."
            raise ValueError(err)
        atoms = []
        for a, p in zip(self._atoms, value):
            a.position = p
            atoms.append(a)
        self._atoms = atoms

    @property
    def symbols(self) -> List[str]:
        return [a.symbol for a in self._atoms]

    @symbols.setter
    def symbols(self, value: List[str]) -> None:
        if len(value) != len(self._atoms):
            err = "Number of symbols must match numbre of atoms."
            raise ValueError(err)
        atoms = []
        for a, s in zip(self._atoms, value):
            a.symbol = s
            atoms.append(a)
        self._atoms = atoms

    @property
    def velocities(self) -> List[np.ndarray]:
        return [a.velocity for a in self._atoms]

    @velocities.setter
    def velocities(self, value: List[np.ndarray]) -> None:
        if len(value) != len(self._atoms):
            err = "Number of velocities must match number of atoms."
            raise ValueError(err)
        atoms = []
        for a, v in zip(self._atoms, value):
            a.velocity = v
            atoms.append(a)
        self._atoms = atoms

    def __iter__(self) -> Generator[Atom, None, None]:
        for a in self._atoms:
            yield a
