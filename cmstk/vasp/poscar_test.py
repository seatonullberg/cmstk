from cmstk.vasp.poscar import PoscarFile
from cmstk.utils import data_directory
import numpy as np
import copy
import os


def test_poscar_file():
    """Tests the initialization of a vasp.PoscarFile object."""
    path = os.path.join(data_directory(), "vasp", "POSCAR")
    poscar = PoscarFile(path)
    poscar.read()

    poscar_writer = PoscarFile("test.poscar")
    poscar_writer.comment = poscar.comment
    poscar_writer.lattice_constant = poscar.lattice_constant
    poscar_writer.total_volume = poscar.total_volume
    poscar_writer.lattice_vectors = poscar.lattice_vectors
    poscar_writer.n_atoms_per_symbol = poscar.n_atoms_per_symbol
    poscar_writer.selective_dynamics = poscar.selective_dynamics
    poscar_writer.coordinate_system = poscar.coordinate_system
    poscar_writer.positions = poscar.positions
    poscar_writer.relaxations = poscar.relaxations
    poscar_writer.write()

    poscar_reader = PoscarFile("test.poscar")
    poscar_reader.read()
    assert poscar_reader.comment == poscar.comment
    assert poscar_reader.lattice_constant == poscar.lattice_constant
    assert poscar_reader.total_volume == poscar.total_volume
    assert np.array_equal(poscar_reader.lattice_vectors,
                          poscar.lattice_vectors)
    assert poscar_reader.n_atoms_per_symbol == poscar.n_atoms_per_symbol
    assert poscar_reader.selective_dynamics == poscar.selective_dynamics
    assert poscar_reader.coordinate_system == poscar.coordinate_system
    assert np.array_equal(poscar_reader.positions,
                          poscar.positions)
    assert np.array_equal(poscar_reader.relaxations,
                          poscar.relaxations)
    os.remove("test.poscar")


def test_poscar_to_cartesian():
    """Tests conversion from direct to cartesian coordinates."""
    path = os.path.join(data_directory(), "vasp", "POSCAR")
    poscar = PoscarFile(path)
    poscar.read()
    orig_positions = copy.deepcopy(poscar.positions)
    # starts as cartesian so convert to direct
    poscar.to_direct()
    poscar.to_cartesian()
    cart_positions = copy.deepcopy(poscar.positions)
    assert np.array_equal(orig_positions, cart_positions)


def test_poscar_to_direct():
    """Tests conversion from cartesian to direct coordinates."""
    path = os.path.join(data_directory(), "vasp", "POSCAR")
    poscar = PoscarFile(path)
    poscar.read()
    orig_shape = copy.deepcopy(poscar.positions.shape)
    poscar.to_direct()
    direct_shape = copy.deepcopy(poscar.positions.shape)
    assert np.max(poscar.positions) <= 1
    assert direct_shape == orig_shape
