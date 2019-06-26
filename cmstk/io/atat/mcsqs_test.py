from cmstk.atat.mcsqs import BestsqsFile
from cmstk.io.atat.mcsqs import bestsqs_to_poscar
from cmstk.utils import data_directory
import os


def test_bestsqs_to_poscar():
    """Tests the conversion of a BestsqsFile object to a PoscarFile object."""
    path = os.path.join(data_directory(), "atat", "bestsqs.out")
    bestsqs = BestsqsFile(path)
    bestsqs.read()
    sym_order = ["Fe", "Cr"]
    poscar = bestsqs_to_poscar(bestsqs, sym_order)
    assert poscar.positions.shape == bestsqs.positions.shape
    assert poscar.lattice_vectors.shape == bestsqs.lattice_vectors.shape
    assert sum(poscar.n_atoms_per_symbol) == len(bestsqs.symbols)
    poscar.write("test.poscar")
    os.remove("test.poscar")