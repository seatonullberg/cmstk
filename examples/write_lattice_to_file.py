from cmstk.lattice import Atom, AtomicPosition, Lattice, ProtoLatticeFile
from cmstk.units import Picometer
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating atoms...")
    start = datetime.now()
    p1 = (Picometer(100.0), Picometer(0.0), Picometer(0.0))
    p1 = AtomicPosition(p1)
    a1 = Atom(symbol="C", position=p1)
    p2 = (Picometer(0.0), Picometer(100.0), Picometer(0.0))
    p2 = AtomicPosition(p2)
    a2 = Atom(symbol="C", position=p2)
    p3 = (Picometer(0.0), Picometer(0.0), Picometer(100.0))
    p3 = AtomicPosition(p3)
    a3 = Atom(symbol="C", position=p3)
    print("Constructing a lattice...")
    lattice = Lattice([a1, a2, a3])
    print("Writing lattice to file...")
    path = "test.lattice"
    lattice.to_file(path=path, t=ProtoLatticeFile)
    end = datetime.now()
    print("Finished writing {}.".format(path))
    print("Total time: {}".format(end-start))
    size = os.path.getsize(path)
    print("{} contains {} atoms and has size: {} bytes".format(path, lattice.n_atoms, size))
