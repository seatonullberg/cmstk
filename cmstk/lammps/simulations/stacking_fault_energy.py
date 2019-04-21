from cmstk.lammps import LAMMPS
from cmstk.lammps.simulations.base import BaseLammpsSimulation


class StackingFaultEnergy(BaseLammpsSimulation):
    """Implementation of a LAMMPS stacking fault simulation.
    
    Args:
        potential (obj): <TODO> eventually this will be an object not a str
        structure (obj): <TODO> eventually pass a Lattice which can be written to lammps format
        - can leave blank for a default implementation ???
    """

    def __init__(self, potential, structure):
        self.potential = potential
        self.structure = structure
        # init the lammps interface
        lammps = LAMMPS()
        equal_vars = []  # TODO
        atom_vars = []  # TODO
        # init the base
        super().__init__(lammps, equal_vars, atom_vars)

    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Tutorial_1
        # TODO: write the script here.
        pass