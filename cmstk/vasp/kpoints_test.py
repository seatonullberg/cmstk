from cmstk.vasp.kpoints import KpointsFile
from cmstk.utils import data_directory
import os


def test_kpoints_file():
    """Tests the initialization of a vasp.KpointsFile object."""
    path = os.path.join(data_directory(), "vasp", "KPOINTS")
    kpoints = KpointsFile(path)
    kpoints.read()

    kpoints_writer = KpointsFile("test.kpoints")
    kpoints_writer.comment = kpoints.comment
    kpoints_writer.n_kpoints = kpoints.n_kpoints
    kpoints_writer.mesh_type = kpoints.mesh_type
    kpoints_writer.mesh_size = kpoints.mesh_size
    kpoints_writer.mesh_shift = kpoints.mesh_shift
    kpoints_writer.write()

    kpoints_reader = KpointsFile("test.kpoints")
    kpoints_reader.read()
    assert kpoints_reader.comment == kpoints.comment
    assert kpoints_reader.n_kpoints == kpoints.n_kpoints
    assert kpoints_reader.mesh_type == kpoints.mesh_type
    assert kpoints_reader.mesh_size == kpoints.mesh_size
    assert kpoints_reader.mesh_shift == kpoints.mesh_shift
    os.remove("test.kpoints")
