from cmstk.atat.mcsqs import BestcorrFile, RndstrFile
import numpy as np
import os


def test_bestcorr_file():
    """Tests initialization of a BestcorrFile object."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "data", "bestcorr.out")

    bestcorr = BestcorrFile(path)
    bestcorr.read()
    assert bestcorr.objective_functions == [-0.997685]
    assert len(bestcorr.clusters) == 1
    assert len(bestcorr.clusters[0]) == 4


def test_rndstr_file():
    """Tests the initialization of a RndstrFile object."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "data", "structures", "rndstr.in")

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
    assert rndstr_reader.lattice_angles == rndstr.lattice_angles
    assert rndstr_reader.lattice_parameters == rndstr.lattice_parameters
    assert np.array_equal(rndstr_reader.lattice_vectors, rndstr.lattice_vectors)
    assert np.array_equal(rndstr_reader.positions, rndstr.positions)
    assert rndstr_reader.probabilities == rndstr.probabilities

    os.remove("test.in")
