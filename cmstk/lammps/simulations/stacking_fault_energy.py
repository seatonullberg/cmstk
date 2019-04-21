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
        # init the lammps interface
        lammps = LAMMPS()
        # extract stacking fault energy
        equal_vars = ["SFE"]
        # no atom style variables
        atom_vars = []
        # init the base
        super().__init__(lammps, equal_vars, atom_vars)

    @property
    def energy(self):
        return self._results["SFE"]

    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Intrinsic_Stacking-Fault_Energy
        # TODO: write the script here.
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
        # init the lammps interface
        lammps = LAMMPS()
        # extract stacking fault energy
        equal_vars = ["SFE"]
        # no atom style variables
        atom_vars = []
        # init the base
        super().__init__(lammps, equal_vars, atom_vars)

    @property
    def energy(self):
        return self._results["SFE"]

    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Extrinsic_Stacking-Fault_Energy
        # TODO: write the script here.
        pass