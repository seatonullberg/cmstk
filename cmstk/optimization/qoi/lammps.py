import type_sanity as ts
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
        ts.is_type((symbols, tuple, "symbols"), 
                   (potential_str, str, "potential_str"), 
                   (structure_str, str, "structure_str"))
        for s in symbols:
            ts.is_type((s, str))
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