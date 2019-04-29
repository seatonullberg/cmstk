from cmstk.lammps import LAMMPS
from cmstk.lammps.simulations.base import BaseLammpsSimulation


class VacancyFormationEnergy(BaseLammpsSimulation):
    """Implementation of a LAMMPS simulation which extracts the energy of vacancy formation.
    
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
        self.add_variable_quantity("Ev", 0)

    @property
    def energy(self):
        return self.quantities["Ev"]["results"]

    # TODO
    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Vacancy_Formation_Energy
        pass


class InterstitialFormationEnergy(BaseLammpsSimulation):
    """Implementation of a LAMMPS simulation which extracts the energy of interstitial formation.
    
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
        self.add_variable_quantity("Ei", 0)

    @property
    def energy(self):
        return self.quantities["Ei"]["results"]

    # TODO
    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Interstitial_Formation_Energy
        pass