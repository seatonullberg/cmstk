from cmstk.structures.atoms import AtomCollection
import numpy as np
from typing import List, Optional


# TODO
class SimulationCell(object):
    """Representation of a collection of AtomCollections to be used in
       any simulation environment.
    """ 
    def __init__(self, collections: Optional[List[AtomCollection]] = None,
                 centroids: Optional[List[np.ndarray]] = None,
                 coordinate_matrix: Optional[np.ndarray] = None,
                 scaling_factor: float = 1.0) -> None:
        pass