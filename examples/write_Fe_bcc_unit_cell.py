from cmstk.lattice import Atom, Lattice
from cmstk.lattice.io import write_lattice_to_proto_file
from cmstk.lattice.unit_cell import unit_cell_bcc
from cmstk.units import Picometer
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating BCC unit cell...")
    start = datetime.now()
    a0 = Picometer(286.65)  # physically accurate
    # requires a custom tolerance because covalent radius is too large to pack BCC in Fe
    # default tolerance would be 264.0
    tol = Picometer(248.0)
    lattice = unit_cell_bcc(a0=a0, symbol="Fe", tolerance=tol)
    print("Writing lattice to file...")
    filename = "Fe_bcc_unit_cell.lattice"
    write_lattice_to_proto_file(path=filename, lattice=lattice)
    end = datetime.now()
    total_time = (end-start).total_seconds()
    print("Total time: {} seconds".format(total_time))
    size = os.path.getsize(filename)
    print("Generated {} ({} bytes)".format(filename, size))