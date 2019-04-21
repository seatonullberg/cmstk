from cmstk.lammps import LAMMPS
from cmstk.lammps.simulations.base import BaseLammpsSimulation


class StructuralMinimization(BaseLammpsSimulation):
    """Implementation of a LAMMPS structural minimization simulation.
    
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
        # extract total energy, lattice parameter, and cohesive energy 
        equal_vars = ["teng", "length", "ecoh"]
        # no atom style variables to extract
        atom_vars = []
        # init the base
        super().__init__(lammps, equal_vars, atom_vars)

    @property
    def total_energy(self):
        return self._results["teng"]

    @property
    def length(self):
        return self._results["length"]

    @property
    def cohesive_energy(self):
        return self._results["ecoh"]

    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Tutorial_1
        # TODO: write the script here.
        pass
