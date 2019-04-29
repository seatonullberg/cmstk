import type_sanity as ts


class BasePotential(object):
    """Representation of a generalized interatomic potential.
    
    Args:
        obj (instance of BasePotential): Used to check implementation of required methods.
        symbols (list of str): List of IUPAC chemical symbols.
        parameters (dict): Fitting parameters.
    
    Attributes:
        symbols (list of str): List of IUPAC chemical symbols.
        parameters (dict): Fitting parameters.
    """

    def __init__(self, obj, symbols, parameters):
        ts.is_type((symbols, list, "symbols"))
        for s in symbols:
            ts.is_type((s, str))
        self.symbols = symbols
        ts.is_type((parameters, dict, "parameters"))
        for k, v in parameters.items():
            if type(k) is not str or type(v) is not float:
                raise TypeError("`parameters` must have keys of type str and values of type float")
        self.parameters = parameters
        ts.is_instance((obj, BasePotential, "obj"))
        ts.implements((obj, "to_lammps", "obj"))
    
    @property 
    def symbol_pairs(self):
        pairs = []
        for i, sym1 in enumerate(self.symbols):
            for j, sym2 in enumerate(self.symbols):
                if i <= j:
                    pairs.append(sym1+sym2)
        return pairs
