from cmstk.lammps import LAMMPS
from cmstk.lammps.simulations.base import BaseLammpsSimulation


class IntrinsicStackingFaultEnergy(BaseLammpsSimulation):
    """Implementation of a LAMMPS intrinsic stacking fault simulation.
    
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
        self.add_variable_quantity("SFE", 0)  # might actually be 1

    @property
    def energy(self):
        return self.quantities["SFE"]["results"]

    # TODO
    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Intrinsic_Stacking-Fault_Energy
        pass


class ExtrinsicStackingFaultEnergy(BaseLammpsSimulation):
    """Implementation of a LAMMPS extrinsic stacking fault simulation.
    
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
        self.add_variable_quantity("SFE", 0)  # might be 1

    @property
    def energy(self):
        return self.quantities["SFE"]["results"]

    # TODO
    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Extrinsic_Stacking-Fault_Energy
        pass