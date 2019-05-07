from cmstk.lattice import Atom, Lattice
from cmstk.units import Picometer
from cmstk.units.vector import Vector3D
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating atoms...")
    start = datetime.now()
    # initialize 4 atoms in a square plane
    p1 = (Picometer(200.0), Picometer(0.0), Picometer(0.0))
    p1 = Vector3D(p1)
    a1 = Atom(symbol="C", position=p1)
    p2 = (Picometer(0.0), Picometer(200.0), Picometer(0.0))
    p2 = Vector3D(p2)
    a2 = Atom(symbol="C", position=p2)
    p3 = (Picometer(200.0), Picometer(200.0), Picometer(0.0))
    p3 = Vector3D(p3)
    a3 = Atom(symbol="C", position=p3)
    p4 = (Picometer(0.0), Picometer(0.0), Picometer(0.0))
    p4 = Vector3D(p4)
    a4 = Atom(symbol="C", position=p4)
    print("Constructing a lattice...")
    # initialize a lattice with the previously defined atoms
    lattice = Lattice([a1, a2, a3, a4])
    print("Writing lattice to file...")
    # write the lattice to a protobuf encoded binary file
    filename = "test.lattice"
    lattice.to_proto(filename)
    end = datetime.now()
    # analyze time and space results
    total_time = (end-start).total_seconds()
    print("Total time: {} seconds".format(total_time))
    size = os.path.getsize(filename)
    print("Generated {} ({} bytes)".format(filename, size))
