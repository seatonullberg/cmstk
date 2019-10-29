from cmstk.structure.atom import Atom, AtomCollection
from cmstk.structure.simulation import SimulationCell
import numpy as np


def test_simulation_cell():
    """Tests initialization of a SimulationCell object."""
    atoms = [
        Atom(position=np.array([0, 0, 0])),
        Atom(position=np.array([1, 1, 1]))
    ]
    collection = AtomCollection(atoms)
    cm = np.array([[2.0, 0, 0], [0, 2.0, 0], [0, 0, 2.0]])
    sf = 2.0
    cell = SimulationCell(collection, cm, sf)
    assert cell.collection.n_atoms == 2
    assert np.array_equal(cell.coordinate_matrix, cm)
    assert cell.scaling_factor == 2.0
