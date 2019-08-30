from cmstk.structures.atoms import Atom, AtomCollection
from cmstk.utils import Number
import numpy as np
from typing import Generator, List, Optional


class Lattice(AtomCollection):
    """Representation of a collection of atoms with crystalline ordering.

    Args:
        angles: The defining angles (alpha, beta, gamma).
        parameters: The defining parameters (a, b, c).
        atoms: The atoms in the collection.
        coordinate_matrix: Parameters and angles combined into a 3x3 matrix.
        tolerance: The radius in which to check from existing atoms.
        vectors: The defining vectors (coordinate system).

    Attributes:
        angles: The defining angles (alpha, beta, gamma).
        atoms: The atoms in the collection.
        coordinate_matrix: Parameters and angles combined into a 3x3 matrix.
        parameters: The defining parameters (a, b, c).
        tolerance: The radius in which to check for atoms on add or remove.
        vectors: The defining vectors (coordinate system).
        
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
                 angles: Optional[np.ndarray] = None,
                 atoms: Optional[List[Atom]] = None,
                 coordinate_matrix: Optional[np.ndarray] = None,
                 parameters: Optional[np.ndarray] = None,
                 tolerance: Optional[Number] = None,
                 vectors: Optional[np.ndarray] = None) -> None:
        super().__init__(atoms, tolerance)
        if angles is None:
            angles = np.array([])
        self.angles = angles
        if parameters is None:
            parameters = np.array([])
        self.parameters = parameters
        if vectors is None:
            vectors = np.identity(3)
        self.vectors = vectors
        self.coordinate_matrix = coordinate_matrix

    @property
    def fractional_positions(self) -> Generator[np.ndarray, None, None]:
        if self.parameters is None:
            err = "`fractional_positions` requires `parameters` to be set."
            raise ValueError(err)
        for position in self.positions:
            yield position / self.parameters
