from cmstk.lammps import LAMMPS
from cmstk.lammps.simulations.base import BaseLammpsSimulation
from cmstk.lammps.test_interface import write_test_file
import os


def test_base_lammps_simulation():
    # tests initialization, execution, and extraction of a LAMMPS simulation
    lammps = LAMMPS()
    simulation = BaseLammpsSimulation(lammps)
    simulation.add_atom_quantity("id", 0, (4000,))
    simulation.add_compute_quantity("test2", 1, 1, (4000,))
    simulation.add_fix_quantity("test3", 1, 2, (4000, 3))
    simulation.add_global_quantity("natoms", 0)
    simulation.add_variable_quantity("test0", 0)
    filename = "test.in"
    write_test_file(filename)
    # TODO: test the other initialization methods
    simulation.simulate(filename=filename)
    for quantity in simulation.quantities:
        assert quantity["result"] is not None
    os.remove("log.lammps")
    os.remove(filename)