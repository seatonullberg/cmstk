from cmstk.vasp.poscar import PoscarFile
from cmstk.io.vasp.poscar import poscar_to_rndstr
from cmstk.utils import data_directory
import numpy as np
import os


def test_poscar_to_rndstr():
    """Tests the conversion of a PoscarFile object to a RndstrFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe75Cr25_BCC_bulk.poscar")
    poscar = PoscarFile(filepath=path)
    poscar.read()
    probabilities = [
        {"Fe": 0.75, "Cr": 0.25} for _ in range(poscar.lattice.n_atoms)
    ]
    vectors = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ])
    rndstr = poscar_to_rndstr(poscar=poscar,
                              probabilities=probabilities,
                              vectors=vectors)
    poscar_positions = np.array([p for p in poscar.lattice.positions])
    rndstr_positions = np.array([p for p in rndstr.lattice.positions])
    assert np.array_equal(poscar_positions, rndstr_positions)
    assert np.array_equal(poscar.lattice.coordinate_matrix,
                          rndstr.lattice.coordinate_matrix)
    rndstr.write("test.rndstr")
    assert os.path.exists("test.rndstr")
    os.remove("test.rndstr")
