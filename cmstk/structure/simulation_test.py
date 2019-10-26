from cmstk.structure.atom import Atom, AtomCollection
from cmstk.structure.simulation import SimulationCell
import numpy as np
import pytest


def test_simulation_cell():
    """Tests initialization of a SimulationCell object."""
    atoms0 = [
        Atom(position=np.array([0, 0, 0])),
        Atom(position=np.array([1, 1, 1]))
    ]
    collection0 = AtomCollection(atoms=atoms0)
    atoms1 = [
        Atom(position=np.array([2, 2, 2])),
        Atom(position=np.array([3, 3, 3])),
    ]
    collection1 = AtomCollection(atoms=atoms1)
    atoms2 = [
        Atom(position=np.array([0, 0, 0])),
        Atom(position=np.array([4, 4, 4]))
    ]
    collection2 = AtomCollection(atoms=atoms2)
    cm = np.array([[2.0, 0, 0], [0, 2.0, 0], [0, 0, 2.0]])
    sf = 2.0
    cell = SimulationCell(collections=[collection0],
                          coordinate_matrix=cm,
                          scaling_factor=sf)
    assert cell.n_collections == 1
    cell.add_collection(collection1)
    assert cell.n_collections == 2
    with pytest.raises(ValueError):
        cell.add_collection(collection2)
    cell.remove_collection(1)
    assert cell.n_collections == 1
