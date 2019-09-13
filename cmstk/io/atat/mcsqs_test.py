from cmstk.atat.mcsqs import BestsqsFile
from cmstk.io.atat.mcsqs import bestsqs_to_poscar
from cmstk.utils import data_directory
import numpy as np
import os


def test_bestsqs_to_poscar():
    """Tests the conversion of a BestsqsFile object to a PoscarFile object."""
    path = os.path.join(data_directory(), "atat",
                        "Fe75Cr25_BCC_bulk.bestsqs.out")
    bestsqs = BestsqsFile(filepath=path)
    bestsqs.read()
    scale = 1.0
    sym_order = ["Fe", "Cr"]
    poscar = bestsqs_to_poscar(bestsqs, scale, sym_order)
    poscar_positions = np.array([p for p in poscar.lattice.positions])
    bestsqs_positions = np.array([p for p in bestsqs.lattice.positions])
    assert np.array_equal(poscar_positions, bestsqs_positions)
    assert np.array_equal(poscar.lattice.coordinate_matrix,
                          bestsqs.lattice.coordinate_matrix)
    assert sum(poscar.n_atoms_per_symbol) == bestsqs.lattice.n_atoms
    poscar.write("test.poscar")
    assert os.path.exists("test.poscar")
    os.remove("test.poscar")
