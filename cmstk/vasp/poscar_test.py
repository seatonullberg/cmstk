from cmstk.vasp.poscar import PoscarFile
import numpy as np
import os


def test_poscar_file():
    """Tests the initialization of a vasp.PoscarFile object."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "data", "structures", "POSCAR")
    poscar = PoscarFile(path)
    poscar.read()

    poscar_writer = PoscarFile("test.poscar")
    poscar_writer.comment = poscar.comment
    poscar_writer.lattice_parameter = poscar.lattice_parameter
    poscar_writer.total_volume = poscar.total_volume
    poscar_writer.lattice_vectors = poscar.lattice_vectors
    poscar_writer.n_atoms_per_species = poscar.n_atoms_per_species
    poscar_writer.selective_dynamics = poscar.selective_dynamics
    poscar_writer.coordinate_system = poscar.coordinate_system
    poscar_writer.positions = poscar.positions
    poscar_writer.relaxations = poscar.relaxations
    poscar_writer.write()

    poscar_reader = PoscarFile("test.poscar")
    poscar_reader.read()
    assert poscar_reader.comment == poscar.comment
    assert poscar_reader.lattice_parameter == poscar.lattice_parameter
    assert poscar_reader.total_volume == poscar.total_volume
    assert np.array_equal(poscar_reader.lattice_vectors,
                          poscar.lattice_vectors)
    assert poscar_reader.n_atoms_per_species == poscar.n_atoms_per_species
    assert poscar_reader.selective_dynamics == poscar.selective_dynamics
    assert poscar_reader.coordinate_system == poscar.coordinate_system
    assert np.array_equal(poscar_reader.positions,
                          poscar.positions)
    assert np.array_equal(poscar_reader.relaxations,
                          poscar.relaxations)
    os.remove("test.poscar")