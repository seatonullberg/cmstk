import type_sanity as ts
from cmstk.lammps import LAMMPS
from cmstk.lammps.simulations.base import BaseLammpsSimulation
from cmstk.potentials.base import BasePotential


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
        lammps = LAMMPS()
        super().__init__(lammps)
        self.add_variable_quantity("teng", 0)    # extract total energy
        self.add_variable_quantity("length", 0)  # extract lattice parameter
        self.add_variable_quantity("ecoh", 0)    # extract cohesive energy

    @property
    def total_energy(self):
        return self.quantities["teng"]["results"]

    @property
    def length(self):
        return self.quantities["length"]["results"]

    @property
    def cohesive_energy(self):
        return self.quantities["ecoh"]["results"]

    # TODO
    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Tutorial_1
        pass