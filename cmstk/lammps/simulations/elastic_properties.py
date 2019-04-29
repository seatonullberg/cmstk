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
        lammps = LAMMPS()
        super().__init__(lammps)
        self.add_variable_quantity("bulkmodulus", 0)
        self.add_variable_quantity("shearmodulus1", 0)
        self.add_variable_quantity("c11", 0)
        self.add_variable_quantity("c12", 0)
        self.add_variable_quantity("c44", 0)

    @property
    def bulk_modulus(self):
        return self.quantities["bulkmodulus"]["results"]

    @property
    def shear_modulus(self):
        return self.quantities["shearmodulus1"]["results"]

    @property
    def c11(self):
        return self.quantities["c11"]["results"]

    @property
    def c12(self):
        return self.quantities["c12"]["results"]

    @property
    def c44(self):
        return self.quantities["c44"]["results"]

    # TODO
    def __str__(self):
        # https://github.com/lammps/lammps/tree/master/examples/ELASTIC
        pass