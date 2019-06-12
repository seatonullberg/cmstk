from cmstk.atat.mcsqs import BestcorrFile, BestsqsFile, RndstrFile
from cmstk.testing_resources import data_directory
import numpy as np
import os


def test_bestcorr_file():
    """Tests initialization of a BestcorrFile object."""
    path = os.path.join(data_directory(), "atat", "bestcorr.out")
    bestcorr = BestcorrFile(path)
    bestcorr.read()
    assert bestcorr.objective_functions == [-0.997685]
    assert len(bestcorr.clusters) == 1
    assert len(bestcorr.clusters[0]) == 4

def test_bestsqs_file():
    """Tests initialization of a BestsqsFile object."""
    path = os.path.join(data_directory(), "atat", "bestsqs.out")
    bestsqs = BestsqsFile(path)
    bestsqs.read()
    lattice_parameters = np.array([10.7, 10.7, 10.7])
    assert np.array_equal(bestsqs.lattice_parameters, lattice_parameters)
    lattice_vectors = np.array([[1.0, 0.0, 0.0],
                                [0.0, 1.0, 0.0],
                                [0.0, 0.0, 1.0]])
    assert np.array_equal(bestsqs.lattice_vectors, lattice_vectors)
    assert bestsqs.positions.shape == (108, 3)
    assert len(bestsqs.symbols) == 108

def test_rndstr_file():
    """Tests the initialization of a RndstrFile object."""
    path = os.path.join(data_directory(), "atat", "rndstr.in")
    rndstr = RndstrFile(path)
    rndstr.read()

    rndstr_writer = RndstrFile("test.in")
    rndstr_writer.lattice_angles = rndstr.lattice_angles
    rndstr_writer.lattice_parameters = rndstr.lattice_parameters
    rndstr_writer.lattice_vectors = rndstr.lattice_vectors
    rndstr_writer.positions = rndstr.positions
    rndstr_writer.probabilities = rndstr.probabilities
    rndstr_writer.write()

    rndstr_reader = RndstrFile("test.in")
    rndstr_reader.read()
    assert np.array_equal(rndstr_reader.lattice_angles, rndstr.lattice_angles)
    assert np.array_equal(rndstr_reader.lattice_parameters, 
                                rndstr.lattice_parameters)
    assert np.array_equal(rndstr_reader.lattice_vectors, rndstr.lattice_vectors)
    assert np.array_equal(rndstr_reader.positions, rndstr.positions)
    assert rndstr_reader.probabilities == rndstr.probabilities

    os.remove("test.in")
