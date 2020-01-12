from cmstk.xyz import XyzFile
from cmstk.util import data_directory
import numpy as np
import os

def test_xyz_file():
    """Test the initialization of a XyzFile."""
    path = os.path.join(data_directory(), "test.xyz")
    xyz = XyzFile(path)
    xyz.load()
    assert xyz.comment == "glucose from 2gbp"
    assert xyz.atom_collection.symbols[0] == "C"
    assert xyz.atom_collection.symbols[-1] == "O"
    position_C = np.array([35.884, 30.895, 49.120])
    position_O = np.array([39.261, 32.018, 46.920])
    assert np.array_equal(xyz.atom_collection.positions[0], position_C)
    assert np.array_equal(xyz.atom_collection.positions[-1], position_O)
    assert xyz.atom_collection.n_atoms == 12
    xyz.atom_collection.remove_atom(position_C)
    xyz.comment = "test"
    xyz.write("test.xyz")
    xyz = XyzFile("test.xyz")
    xyz.load()
    assert xyz.comment == "test"
    assert xyz.atom_collection.symbols[0] == "C"
    assert xyz.atom_collection.symbols[-1] == "O"
    assert xyz.atom_collection.n_atoms == 11
    xyz.unload()
    os.remove("test.xyz")
