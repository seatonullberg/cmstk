from cmstk.atat.mcsqs import BestcorrFile, BestsqsFile, RndstrFile
from cmstk.units.angle import AngleUnit, Degree
from cmstk.units.base import UnitSchema
from cmstk.units.distance import DistanceUnit, Angstrom
from cmstk.utils import data_directory
import numpy as np
import os

unit_schema = UnitSchema(
    (DistanceUnit, Angstrom),
    (AngleUnit, Degree)
)

def test_bestcorr_file():
    """Tests initialization of a BestcorrFile object."""
    path = os.path.join(data_directory(), "atat",
                        "Fe75Cr25_BCC_bulk.bestcorr.out")
    bestcorr = BestcorrFile(filepath=path)
    bestcorr.read()
    assert bestcorr.objective_functions == [-1.099145]
    assert len(bestcorr.clusters) == 1
    assert len(bestcorr.clusters[0]) == 4


def test_bestsqs_file():
    """Tests initialization of a BestsqsFile object."""
    path = os.path.join(data_directory(), "atat",
                        "Fe75Cr25_BCC_bulk.bestsqs.out")
    bestsqs = BestsqsFile(filepath=path)
    bestsqs.read(unit_schema=unit_schema)
    coordinate_matrix_x = np.array([5.7, 0, 0])
    coordinate_matrix_y = np.array([0, 5.7, 0])
    coordinate_matrix_z = np.array([0, 0, 5.7])
    assert np.array_equal(bestsqs.lattice.coordinate_matrix[0].to_ndarray(),
                          coordinate_matrix_x)
    assert np.array_equal(bestsqs.lattice.coordinate_matrix[1].to_ndarray(),
                          coordinate_matrix_y)
    assert np.array_equal(bestsqs.lattice.coordinate_matrix[2].to_ndarray(),
                          coordinate_matrix_z)
    lattice_vectors = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])
    assert np.array_equal(bestsqs.lattice.vectors, lattice_vectors)
    positions = [p for p in bestsqs.lattice.positions]
    assert len(positions) == 16
    assert bestsqs.lattice.n_atoms == 16


def test_rndstr_file():
    """Tests the initialization of a RndstrFile object."""
    path = os.path.join(data_directory(), "atat", "Fe75Cr25_BCC_bulk.rndstr.in")
    rndstr = RndstrFile(filepath=path)
    rndstr.read(unit_schema=unit_schema)

    rndstr_writer = RndstrFile(filepath="test.in")
    rndstr_writer.lattice = rndstr.lattice
    rndstr_writer.probabilities = rndstr.probabilities
    rndstr_writer.write()

    rndstr_reader = RndstrFile(filepath="test.in")
    rndstr_reader.read(unit_schema=unit_schema)
    assert np.array_equal(rndstr_reader.lattice.angles.to_ndarray(), 
                          rndstr.lattice.angles.to_ndarray())
    assert np.array_equal(rndstr_reader.lattice.parameters.to_ndarray(),
                          rndstr.lattice.parameters.to_ndarray())
    assert np.array_equal(rndstr_reader.lattice.vectors, 
                          rndstr.lattice.vectors)
    reader_positions = np.array([p.to_ndarray() for p in rndstr_reader.lattice.positions])
    positions = np.array([p.to_ndarray() for p in rndstr.lattice.positions])
    assert np.array_equal(reader_positions, positions)
    assert rndstr_reader.probabilities == rndstr.probabilities

    os.remove("test.in")
