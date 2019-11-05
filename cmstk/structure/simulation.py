from cmstk.structure.atom import AtomCollection
import numpy as np
from typing import Optional


class SimulationCell(object):
    """Representation of an AtomCollections in any simulation environment.

    Args:
        collection: The AtomCollection to store in the cell.
        coordinate_matrix: Length and angle parameters combined in a 3x3 matrix.
        scaling_factor: Universal scaling factor (lattice constant).
    """

    def __init__(self,
                 collection: Optional[AtomCollection] = None,
                 coordinate_matrix: Optional[np.ndarray] = None,
                 scaling_factor: float = 1.0) -> None:
        if collection is None:
            collection = AtomCollection()
        self.collection = collection
        if coordinate_matrix is None:
            coordinate_matrix = np.identity(3)
        self.coordinate_matrix = coordinate_matrix
        self.scaling_factor = scaling_factor

    # TODO: methods to generate a coordinate_matrix from an AtomCollection
    # rather than a generic default
