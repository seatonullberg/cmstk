from cmstk.atat.mcsqs import BestsqsFile
from cmstk.synergy.atat.mcsqs import bestsqs_to_poscar
from cmstk.util import data_directory
import numpy as np
import os


def test_bestsqs_to_poscar():
    """Tests the conversion of a BestsqsFile object to a PoscarFile object."""
    path = os.path.join(data_directory(), "atat",
                        "Fe75Cr25_BCC_bulk.bestsqs.out")
    bestsqs = BestsqsFile(filepath=path)
    bestsqs.read()
    sym_order = ["Fe", "Cr"]
    poscar = bestsqs_to_poscar(bestsqs, sym_order)
    poscar_positions = np.array([p for p in poscar.simulation_cell.collection.positions])
    bestsqs_positions = np.array([p for p in bestsqs.simulation_cell.collection.positions])
    assert np.array_equal(poscar_positions, bestsqs_positions)
    assert np.array_equal(poscar.simulation_cell.coordinate_matrix,
                          bestsqs.simulation_cell.coordinate_matrix)
    assert poscar.n_atoms_per_symbol[0] == 12
    assert poscar.n_atoms_per_symbol[1] == 4
    poscar.write("test.poscar")
    assert os.path.exists("test.poscar")
    os.remove("test.poscar")
