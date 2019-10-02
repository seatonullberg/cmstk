from cmstk.vasp.poscar import PoscarFile
from cmstk.utils import data_directory
import numpy as np
import os


def test_poscar_file():
    """Tests the initialization of a vasp.PoscarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe75Cr25_BCC_bulk.poscar")
    poscar = PoscarFile(path)
    poscar.read()
    poscar_writer = PoscarFile(filepath="test.poscar",
                               comment=poscar.comment,
                               direct=poscar.direct,
                               lattice=poscar.lattice,
                               n_atoms_per_symbol=poscar.n_atoms_per_symbol,
                               relaxations=poscar.relaxations,
                               scaling_factor=poscar.scaling_factor)
    poscar_writer.write()
    poscar_reader = PoscarFile("test.poscar")
    poscar_reader.read()
    assert poscar_reader.comment == poscar.comment
    assert poscar_reader.direct == poscar.direct
    assert np.array_equal(poscar_reader.lattice.coordinate_matrix,
                          poscar.lattice.coordinate_matrix)
    reader_positions = np.array([p for p in poscar_reader.lattice.positions])
    positions = np.array([p for p in poscar.lattice.positions])
    assert np.array_equal(reader_positions, positions)
    assert len(positions) > 0
    reader_velocities = np.array([v for v in poscar_reader.lattice.velocities])
    velocities = np.array([v for v in poscar.lattice.velocities])
    assert np.array_equal(reader_velocities, velocities)
    assert poscar_reader.n_atoms_per_symbol == poscar.n_atoms_per_symbol
    assert np.array_equal(poscar_reader.relaxations, poscar.relaxations)
    assert poscar_reader.scaling_factor == poscar.scaling_factor
    assert os.path.exists("test.poscar")
    os.remove("test.poscar")

def test_contcar_file():
    """Tests the initialization of a vasp.PoscarFile object reading a CONTCAR."""
    path = os.path.join(data_directory(), "vasp", "Fe75Cr25_BCC_bulk.contcar")
    contcar = PoscarFile(path)
    contcar.read()
    contcar_writer = PoscarFile(filepath="test.contcar",
                               comment=contcar.comment,
                               direct=contcar.direct,
                               lattice=contcar.lattice,
                               n_atoms_per_symbol=contcar.n_atoms_per_symbol,
                               relaxations=contcar.relaxations,
                               scaling_factor=contcar.scaling_factor)
    contcar_writer.write()
    contcar_reader = PoscarFile("test.contcar")
    contcar_reader.read()
    assert contcar_reader.comment == contcar.comment
    assert contcar_reader.direct == contcar.direct
    assert np.array_equal(contcar_reader.lattice.coordinate_matrix,
                          contcar.lattice.coordinate_matrix)
    reader_positions = np.array([p for p in contcar_reader.lattice.positions])
    positions = np.array([p for p in contcar.lattice.positions])
    assert np.array_equal(reader_positions, positions)
    assert len(positions) > 0
    reader_velocities = np.array([v for v in contcar_reader.lattice.velocities])
    velocities = np.array([v for v in contcar.lattice.velocities])
    assert np.array_equal(reader_velocities, velocities)
    assert len(velocities) > 0
    assert contcar_reader.n_atoms_per_symbol == contcar.n_atoms_per_symbol
    assert np.array_equal(contcar_reader.relaxations, contcar.relaxations)
    assert contcar_reader.scaling_factor == contcar.scaling_factor
    assert os.path.exists("test.contcar")
    os.remove("test.contcar")