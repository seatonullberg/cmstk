from cmstk.vasp.poscar import PoscarFile
from cmstk.util import data_directory
import numpy as np
import os


def test_poscar_file():
    """Tests the initialization of a vasp.PoscarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe75Cr25_BCC_bulk.poscar")
    poscar = PoscarFile(path)
    poscar.load()
    poscar_writer = PoscarFile(filepath="test.poscar",
                               comment=poscar.comment,
                               direct=poscar.direct,
                               scaling_factor=poscar.scaling_factor,
                               simulation_cell=poscar.simulation_cell,
                               n_atoms_per_symbol=poscar.n_atoms_per_symbol,
                               relaxations=poscar.relaxations)
    poscar_writer.write()
    poscar_reader = PoscarFile("test.poscar")
    poscar_reader.load()
    assert poscar_reader.comment == poscar.comment
    assert poscar_reader.direct == poscar.direct
    assert np.array_equal(poscar_reader.simulation_cell.coordinate_matrix,
                          poscar.simulation_cell.coordinate_matrix)
    reader_positions = np.array(
        [p for p in poscar_reader.simulation_cell.positions])
    positions = np.array([p for p in poscar.simulation_cell.positions])
    assert np.array_equal(reader_positions, positions)
    assert len(positions) > 0
    assert poscar_reader.n_atoms_per_symbol == poscar.n_atoms_per_symbol
    assert np.array_equal(poscar_reader.relaxations, poscar.relaxations)
    assert poscar_reader.scaling_factor == poscar.scaling_factor
    assert os.path.exists("test.poscar")
    os.remove("test.poscar")


def test_contcar_file():
    """Tests the initialization of a vasp.PoscarFile object from a CONTCAR file."""
    path = os.path.join(data_directory(), "vasp", "Fe75Cr25_BCC_bulk.contcar")
    poscar = PoscarFile(path)
    poscar.load()
    poscar_writer = PoscarFile(filepath="test.contcar",
                               comment=poscar.comment,
                               direct=poscar.direct,
                               scaling_factor=poscar.scaling_factor,
                               simulation_cell=poscar.simulation_cell,
                               n_atoms_per_symbol=poscar.n_atoms_per_symbol,
                               relaxations=poscar.relaxations)
    poscar_writer.write()
    poscar_reader = PoscarFile("test.contcar")
    poscar_reader.load()
    assert poscar_reader.comment == poscar.comment
    assert poscar_reader.direct == poscar.direct
    assert np.array_equal(poscar_reader.simulation_cell.coordinate_matrix,
                          poscar.simulation_cell.coordinate_matrix)
    reader_positions = np.array(
        [p for p in poscar_reader.simulation_cell.positions])
    positions = np.array([p for p in poscar.simulation_cell.positions])
    assert np.array_equal(reader_positions, positions)
    assert len(positions) > 0
    assert poscar_reader.n_atoms_per_symbol == poscar.n_atoms_per_symbol
    assert np.array_equal(poscar_reader.relaxations, poscar.relaxations)
    assert poscar_reader.scaling_factor == poscar.scaling_factor
    assert os.path.exists("test.contcar")
    os.remove("test.contcar")
