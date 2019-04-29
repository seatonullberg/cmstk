

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
        if type(symbols) is not list:
            raise TypeError("`symbols` must be of type list")
        for s in symbols:
            if type(s) is not str:
                raise TypeError("all members of `symbols` must be of type str")
        self.symbols = symbols
        if type(parameters) is not dict:
            raise TypeError("`parameters` must be of type dict")
        for k, v in parameters.items():
            if type(k) is not str or type(v) is not float:
                raise TypeError("`parameters` must have keys of type str and values of type float")
        self.parameters = parameters

        if not isinstance(obj, BasePotential):
            raise TypeError("`obj` must be an instance of type BasePotential")
        obj_methods = [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]
        if "to_lammps" not in obj_methods:
            raise ValueError("`obj` must implement a method called `to_lammps`")
    
    @property 
    def symbol_pairs(self):
        pairs = []
        for i, sym1 in enumerate(self.symbols):
            for j, sym2 in enumerate(self.symbols):
                if i <= j:
                    pairs.append(sym1+sym2)
        return pairs
