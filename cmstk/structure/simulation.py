from cmstk.structure.atom import AtomCollection
import copy
import numpy as np
from typing import List, Optional


class SimulationCell(object):
    """Representation of a collection of AtomCollections to be used in
       any simulation environment.

    Args:
        collections: The AtomCollections to store in the cell.
        coordinate_matrix: Length and angle parameters combined in a 3x3 matrix.
        scaling_factor: Universal scaling constant (lattice constant).
        tolerance: The radius in which to check for existing atoms.
    """

    def __init__(self,
                 collections: Optional[List[AtomCollection]] = None,
                 coordinate_matrix: Optional[np.ndarray] = None,
                 scaling_factor: float = 1.0,
                 tolerance: float = 0.001) -> None:
        self._collections: List[AtomCollection] = []
        if collections is None:
            collections = []
        self.collections = collections
        if coordinate_matrix is None:
            coordinate_matrix = np.identity(3)
        self.coordinate_matrix = coordinate_matrix
        self.scaling_factor = scaling_factor
        self.tolerance = tolerance

    def add_collection(self, collection: AtomCollection) -> None:
        """Adds an AtomCollection to the cell if none of its atoms interfere 
           with existing ones.
      
        Args:
            collection: The AtomCollection to add.

        Raises:
            ValueError
            - An atom exists within the tolerance radius.
        """
        existing_atoms = [a for c in self._collections for a in c.atoms]
        for e_atom in existing_atoms:
            for new_atom in collection.atoms:
                distance = np.sum(
                    np.sqrt((new_atom.position - e_atom.position)**2))
                if distance < self.tolerance:
                    err = "An atom exists within the tolerance radius ({}).".format(
                        self.tolerance)
                    raise ValueError(err)
        self._collections.append(collection)

    def remove_collection(self, index: int) -> AtomCollection:
        """Removes an AtomCollection from the cell and returns it.
      
        Args:
            index: List index of the collection in the cell.
            - It is up to the user to track addition order.
      
        Raises:
            ValueError:
            - There are no collections in the cell.
        """
        if self.n_collections == 0:
            err = "There are no collections in the cell."
            raise ValueError(err)
        # leave the raw index error in the event of an unchecked access
        collection = copy.deepcopy(self._collections[index])
        del self._collections[index]
        return collection

    @property
    def collections(self) -> List[AtomCollection]:
        return copy.deepcopy(self._collections)

    @collections.setter
    def collections(self, value: List[AtomCollection]) -> None:
        self._collections = []
        for v in value:
            self.add_collection(v)

    @property
    def n_collections(self) -> int:
        return len(self._collections)
