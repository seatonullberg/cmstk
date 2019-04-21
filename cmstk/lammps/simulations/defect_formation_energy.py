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
        # init the lammps interface
        lammps = LAMMPS()
        # extract vacancy formation energy
        equal_vars = ["Ev"]
        # no atom style variables to extract
        atom_vars = []
        # init the base
        super().__init__(lammps, equal_vars, atom_vars)

    @property
    def energy(self):
        return self._results["Ev"]

    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Vacancy_Formation_Energy
        # TODO: write the script here.
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
        # init the lammps interface
        lammps = LAMMPS()
        # extract interstitial formation energy
        equal_vars = ["Ei"]
        # no atom style variables to extract
        atom_vars = []
        # init the base
        super().__init__(lammps, equal_vars, atom_vars)

    @property
    def energy(self):
        return self._results["Ei"]

    def __str__(self):
        # https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Interstitial_Formation_Energy
        # TODO: write the script here.
        pass