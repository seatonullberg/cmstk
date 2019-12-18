from cmstk.structure.atom import Atom
from cmstk.structure.simulation import SimulationCell
import numpy as np


def test_simulation_cell():
    """Tests initialization of a SimulationCell object."""
    atoms = [
        Atom(position=np.array([0, 0, 0])),
        Atom(position=np.array([1, 1, 1]))
    ]
    cell = SimulationCell(atoms=atoms)
    assert cell.n_atoms == 2