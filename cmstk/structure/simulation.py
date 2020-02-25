from cmstk.structure.atom import Atom, AtomCollection
import numpy as np
from typing import List, Optional


class SimulationCell(AtomCollection):
    """Representation of atoms in a bounding box.

    Args:
        atoms: The atoms in the collection.
        coordinate_matrix: 3x3 matrix defining the coordinate system of the
            bounding box.
        tolerance: The radius in which to check for atoms on add or remove.
    """
    def __init__(self,
                 atoms: Optional[List[Atom]] = None,
                 coordinate_matrix: Optional[np.ndarray] = None,
                 tolerance: float = 0.001) -> None:
        if coordinate_matrix is None:
            coordinate_matrix = np.identity(3)
        self.coordinate_matrix = coordinate_matrix
        super().__init__(atoms, tolerance)
