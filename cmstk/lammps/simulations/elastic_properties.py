from cmstk.lammps import LAMMPS
from cmstk.lammps.simulations.base import BaseLammpsSimulation


class ElasticProperties(BaseLammpsSimulation):
    """Implementation of a LAMMPS simulation to extract elastic properties.
    
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
        # extract bulk modulus, shear modulus, c11, c12, and c44
        equal_vars = ["bulkmodulus", "shearmodulus1", "c11", "c12", "c44"]
        # no atomic style variables
        atom_vars = []
        # init the base
        super().__init__(lammps, equal_vars, atom_vars)

    @property
    def bulk_modulus(self):
        return self._results["bulkmodulus"]

    @property
    def shear_modulus(self):
        return self._results["shearmodulus1"]

    @property
    def c11(self):
        return self._results["c11"]

    @property
    def c12(self):
        return self._results["c12"]

    @property
    def c44(self):
        return self._results["c44"]

    def __str__(self):
        # https://github.com/lammps/lammps/tree/master/examples/ELASTIC
        # TODO: write the script here.
        pass