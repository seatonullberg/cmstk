from cmstk.lattice import Atom, AtomicPosition, Lattice
from cmstk.lattice.io import write_lattice_to_proto_file
from cmstk.lattice.unit_cell import unit_cell_fcc
from cmstk.units import Picometer
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating unit cell...")
    start = datetime.now()
    a0 = Picometer(352.4)
    lattice = unit_cell_fcc(a0=a0, symbol="Ni")
    print("Writing lattice to file...")
    filename = "Ni_fcc_unit_cell.lattice"
    write_lattice_to_proto_file(path=filename, lattice=lattice)
    end = datetime.now()
    print("Finished writing {}.".format(filename))
    total_time = (end-start).total_seconds()
    print("Total time: {} seconds".format(total_time))
    size = os.path.getsize(filename)
    print("{} contains {} atoms and has size: {} bytes".format(filename, lattice.n_atoms, size))
