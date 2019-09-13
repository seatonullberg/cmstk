from cmstk.structures.atoms import Atom, AtomCollection
from cmstk.utils import Number
import numpy as np
from typing import Generator, List, Optional


class Lattice(AtomCollection):
    """Representation of a collection of atoms with crystalline ordering.

    Args:
        atoms: The atoms in the collection.
        coordinate_matrix: Parameters and angles combined into a 3x3 matrix.
        tolerance: The radius in which to check from existing atoms.

    Attributes:
        atoms: The atoms in the collection.
        coordinate_matrix: Parameters and angles combined into a 3x3 matrix.
        tolerance: The radius in which to check for atoms on add or remove.
        
        Inhereted:
            charges: Electronic charge of each atom.
            fractional_positions: Positions scaled by the parameters.
            magnetic_moments: Magnetic moment of each atom.
            n_atoms: Number of atoms in the collection.
            n_symbols: Number of symbols in the collection.
            positions: Position in space of each atom.
            symbols: IUPAC chemical symbol of each atom.
            velocities: Velocity vector of each atom.
    """
    def __init__(self,
                 atoms: Optional[List[Atom]] = None,
                 coordinate_matrix: Optional[np.ndarray] = None,
                 tolerance: Optional[Number] = None) -> None:
        super().__init__(atoms, tolerance)
        if coordinate_matrix is None:
            coordinate_matrix = np.identity(3)
        self.coordinate_matrix = coordinate_matrix

    @property
    def fractional_positions(self) -> Generator[np.ndarray, None, None]:
        parameters = np.array(
            [np.linalg.norm(row) for row in self.coordinate_matrix])
        for position in self.positions:
            yield position / parameters
