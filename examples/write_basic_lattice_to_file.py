from cmstk.lattice import Atom, AtomicPosition, Lattice
from cmstk.lattice.io import write_lattice_to_proto_file
from cmstk.units import Picometer
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating atoms...")
    start = datetime.now()
    # initialize 4 atoms in a square plane
    p1 = (Picometer(100.0), Picometer(0.0), Picometer(0.0))
    p1 = AtomicPosition(p1)
    a1 = Atom(symbol="C", position=p1)
    p2 = (Picometer(0.0), Picometer(100.0), Picometer(0.0))
    p2 = AtomicPosition(p2)
    a2 = Atom(symbol="C", position=p2)
    p3 = (Picometer(0.0), Picometer(0.0), Picometer(100.0))
    p3 = AtomicPosition(p3)
    a3 = Atom(symbol="C", position=p3)
    p4 = (Picometer(0.0), Picometer(0.0), Picometer(0.0))
    p4 = AtomicPosition(p4)
    a4 = Atom(symbol="C", position=p4)
    print("Constructing a lattice...")
    # initialize a lattice with the previously defined atoms
    lattice = Lattice([a1, a2, a3, a4])
    print("Writing lattice to file...")
    # write the lattice to a protobuf encoded binary file
    filename = "test.lattice"
    write_lattice_to_proto_file(path=filename, lattice=lattice)
    end = datetime.now()
    print("Finished writing {}.".format(filename))
    # analyze time and space results
    total_time = (end-start).total_seconds()
    print("Total time: {} seconds".format(total_time))
    size = os.path.getsize(filename)
    print("{} contains {} atoms and has size: {} bytes".format(filename, lattice.n_atoms, size))
