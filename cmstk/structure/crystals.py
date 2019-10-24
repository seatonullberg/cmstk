from cmstk.structure.atom import Atom, AtomCollection
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
        
        Inherited:
            charges: Electronic charge of each atom.
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
                 tolerance: float = 0.001) -> None:
        super().__init__(atoms, tolerance)
        if coordinate_matrix is None:
            coordinate_matrix = np.identity(3)
        self.coordinate_matrix = coordinate_matrix

    def fractional_positions(self) -> Generator[np.ndarray, None, None]:
        """Returns the position of each atom in the lattice scaled by the length
           of the lattice parameters."""
        parameters = np.array(
            [np.linalg.norm(row) for row in self.coordinate_matrix])
        for position in self.positions:
            yield position / parameters

    def surface_area(self, scaling_factor: float = 1.0) -> float:
        """Returns the surface area of the lattice.
        
        Args:
            scaling_factor: Multiplicative scaling factor applied to both the x 
            and y vectors.
        """
        x = self.coordinate_matrix[0] * scaling_factor
        y = self.coordinate_matrix[1] * scaling_factor
        magx = np.linalg.norm(x)
        magy = np.linalg.norm(y)
        ux = x / magx
        uy = y / magy
        theta = np.arccos(np.clip(np.dot(ux, uy), -1.0, 1.0))
        return magx * magy * np.sin(theta)
