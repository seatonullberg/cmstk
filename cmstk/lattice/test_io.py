from cmstk.lattice.base import Atom, AtomicPosition, Lattice
from cmstk.lattice.io import write_lattice_to_proto_file, read_lattice_from_proto_file
from cmstk.units.distance import Picometer
import os


def test_lattice_to_from_proto():
    # tests if Lattice can be written to protobuf file
    # tests if Lattice can be initialized from protobuf file
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = AtomicPosition(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    assert l.n_atoms == 1
    filename = "test.lattice"
    write_lattice_to_proto_file(path=filename, lattice=l)
    assert os.path.exists("test.lattice")
    new_l = read_lattice_from_proto_file(path=filename)
    assert new_l.n_atoms == 1
    os.remove("test.lattice")