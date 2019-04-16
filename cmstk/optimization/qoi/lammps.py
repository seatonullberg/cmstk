from cmstk.optimization.qoi.base import BaseQOI


class LammpsQOI(BaseQOI):
    """Representation of a quantity of interest which is calculated via LAMMPS.
    
    Args:
        symbols (tuple of str): IUPAC chemical symbols.
        potential_str (str): LAMMPS style potential definition.
        structure_str (str): LAMMPS style structure definition.
        name (str): Unique and descriptive identifier.
        target (float): Target value to optimize towards.
        parameters (numpy.ndarray): Parameter set used for evaluation.
    """

    def __init__(self, symbols, potential_str, structure_str,
                 name, target, parameters):
        super().__init__(self, name, target, parameters)
        
        if type(symbols) is not tuple:
            raise TypeError("`symbols` must be of type tuple")
        for s in symbols:
            if type(s) is not str:
                raise TypeError("all members of `symbols` must be of type str")
        if type(potential_str) is not str:
            raise TypeError("`potential_str` must be of type str")
        if type(structure_str) is not str:
            raise TypeError("`structure_str` must be of type str")

        self._symbols = symbols
        self._potential_str = potential_str
        self._structure_str = structure_str


class LammpsCohesiveEnergy(LammpsQOI): pass


class LammpsLatticeParameter(LammpsQOI): pass


class LammpsC11(LammpsQOI): pass


class LammpsC12(LammpsQOI): pass


class LammpsC44(LammpsQOI): pass


class LammpsBulkModulus(LammpsQOI): pass


class LammpsShearModulus(LammpsQOI): pass


class LammpsStackingFaultEnergy(LammpsQOI): pass


class LammpsVacancyEnergy(LammpsQOI): pass


class LammpsPhaseOrderFCC(LammpsQOI): pass


class LammpsPhaseOrderBCC(LammpsQOI): pass