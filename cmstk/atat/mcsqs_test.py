from cmstk.atat.mcsqs import BestcorrFile, BestsqsFile, RndstrFile
from cmstk.utils import data_directory
import numpy as np
import os


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
    bestsqs.read()
    coordinate_matrix = np.array([[5.7, 0, 0], [0, 5.7, 0], [0, 0, 5.7]])
    assert np.array_equal(bestsqs.lattice.coordinate_matrix, coordinate_matrix)
    lattice_vectors = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])
    assert np.array_equal(bestsqs.lattice.vectors, lattice_vectors)
    positions = [p for p in bestsqs.lattice.positions]
    assert len(positions) == 16
    assert bestsqs.lattice.n_atoms == 16


def test_rndstr_file():
    """Tests the initialization of a RndstrFile object."""
    path = os.path.join(data_directory(), "atat",
                        "Fe75Cr25_BCC_bulk.rndstr.in")
    rndstr = RndstrFile(filepath=path)
    rndstr.read()

    rndstr_writer = RndstrFile(filepath="test.in")
    rndstr_writer.lattice = rndstr.lattice
    rndstr_writer.probabilities = rndstr.probabilities
    rndstr_writer.write()

    rndstr_reader = RndstrFile(filepath="test.in")
    rndstr_reader.read()
    assert np.array_equal(rndstr_reader.lattice.angles, rndstr.lattice.angles)
    assert np.array_equal(rndstr_reader.lattice.parameters,
                          rndstr.lattice.parameters)
    assert np.array_equal(rndstr_reader.lattice.vectors,
                          rndstr.lattice.vectors)
    reader_positions = np.array([p for p in rndstr_reader.lattice.positions])
    positions = np.array([p for p in rndstr.lattice.positions])
    assert np.array_equal(reader_positions, positions)
    assert rndstr_reader.probabilities == rndstr.probabilities

    os.remove("test.in")
