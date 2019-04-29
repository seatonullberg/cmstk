from cmstk.potentials.base import BasePotential


class LennardJonesPotential(BasePotential):
    """Implementation of the Lennard-Jones potential.
    
    Args:
        symbols (list of str): List of IUPAC chemical symbols.
        parameters (dict): Fitting parameters.
        cutoff (float): The cutoff distance
    
    Attributes:
        symbols (list of str): List of IUPAC chemical symbols.
        parameters (dict): Fitting parameters.
    """

    def __init__(self, symbols, parameters, cutoff):
        if type(cutoff) is not float:
            raise TypeError("`cutoff` must be of type float")
        self._cutoff = cutoff
        super().__init__(self, symbols, parameters)

    def to_lammps(self):
        s = "pair_style lj/cut {}\n".format(self._cutoff)
        s += "pair_coeff * * {} {} {}\n".format(self.parameters["a"],
                                                self.parameters["b"],
                                                self._cutoff)
        return s