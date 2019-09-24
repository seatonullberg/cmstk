from cmstk.structures.atoms import Atom
from cmstk.structures.crystals import Lattice
import numpy as np


def test_lattice():
    """Tests initialization of a Lattice object."""
    atoms = [
        Atom(position=np.array([0, 0, 0])),
        Atom(position=np.array([1, 1, 1]))
    ]
    cm = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
    lattice = Lattice(atoms=atoms, coordinate_matrix=cm)
    fractional_positions = [f for f in lattice.fractional_positions()]
    assert fractional_positions[0][0] == 0
    assert fractional_positions[1][0] == 0.5
    assert lattice.surface_area() == 4.0
