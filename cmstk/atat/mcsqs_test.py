from cmstk.atat.mcsqs import BestcorrFile, BestsqsFile, RndstrFile
from cmstk.util import data_directory
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
    bestcorr.clear()
    assert len(bestcorr.clusters) == 0
    assert len(bestcorr.objective_functions) == 0


def test_bestsqs_file():
    """Tests initialization of a BestsqsFile object."""
    path = os.path.join(data_directory(), "atat",
                        "Fe75Cr25_BCC_bulk.bestsqs.out")
    bestsqs = BestsqsFile(filepath=path)
    bestsqs.read()
    cm = np.array([[5.7, 0, 0], [0, 5.7, 0], [0, 0, 5.7]])
    assert np.array_equal(bestsqs.simulation_cell.coordinate_matrix, cm)
    lattice_vectors = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])
    assert np.array_equal(bestsqs.vectors, lattice_vectors)
    assert len(bestsqs.simulation_cell.collection.positions) == 16
    assert bestsqs.simulation_cell.collection.n_atoms == 16
    bestsqs.clear()
    assert bestsqs.simulation_cell.collection.n_atoms == 0
    assert len(bestsqs.vectors) == 0


def test_rndstr_file():
    """Tests the initialization of a RndstrFile object."""
    path = os.path.join(data_directory(), "atat", "Fe75Cr25_BCC_bulk.rndstr.in")
    rndstr = RndstrFile(filepath=path)
    rndstr.read()

    rndstr_writer = RndstrFile(filepath="test.in")
    rndstr_writer.simulation_cell = rndstr.simulation_cell
    rndstr_writer.probabilities = rndstr.probabilities
    rndstr_writer.vectors = rndstr.vectors
    rndstr_writer.write()

    rndstr_reader = RndstrFile(filepath="test.in")
    rndstr_reader.read()
    assert np.array_equal(rndstr_reader.simulation_cell.coordinate_matrix,
                          rndstr.simulation_cell.coordinate_matrix)
    assert np.array_equal(rndstr_reader.vectors, rndstr.vectors)
    reader_positions = rndstr_reader.simulation_cell.collection.positions
    positions = rndstr.simulation_cell.collection.positions
    assert np.array_equal(reader_positions, positions)
    assert rndstr_reader.probabilities == rndstr.probabilities
    os.remove("test.in")
    rndstr.clear()
    assert rndstr.simulation_cell.collection.n_atoms == 0
    assert len(rndstr.probabilities) == 0
    assert len(rndstr.vectors) == 0
