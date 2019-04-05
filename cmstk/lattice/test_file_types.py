from cmstk.lattice.base import Atom, AtomicPosition, Lattice
from cmstk.lattice.file_types import ProtoLatticeFile
from cmstk.units.distance import Picometer
import os


def test_lattice_to_file_proto():
    # tests if Lattice can write itself to protobuf format
    l = Lattice([])
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = AtomicPosition(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    l.to_file("test.lattice", ProtoLatticeFile)
    assert os.path.exists("test.lattice")
    os.remove("test.lattice")