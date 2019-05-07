from cmstk.lattice import Atom, Lattice
from cmstk.lattice.unit_cell import unit_cell_fcc
from cmstk.units import Picometer
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating FCC unit cell...")
    start = datetime.now()
    a0 = Picometer(352.4)  # physically accurate
    lattice = unit_cell_fcc(a0=a0, symbol="Ni")
    print("Writing lattice to file...")
    filename = "Ni_fcc_unit_cell.lattice"
    lattice.to_proto(filename)
    end = datetime.now()
    total_time = (end-start).total_seconds()
    print("Total time: {} seconds".format(total_time))
    size = os.path.getsize(filename)
    print("Generated {} ({} bytes)".format(filename, size))
