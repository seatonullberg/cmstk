import numpy as np


class BaseTag(object):
    """Representation of a generic INCAR tag.
    
    Args:
        comment (str): Description of the tag.
        name (str): VASP compliant tag name.
        valid_options (iterable): The values this tag accepts.
        value (object): Value assigned to the tag.
    """

    def __init__(self, comment, name, valid_options, value):
        assert type(comment) is str
        self._comment = comment
        assert type(name) is str
        self._name = name
        # valid_options can take many forms
        # value can take many forms
        self._valid_options
        self.value = value  # do necessary checks on assignment

    def to_str(self):
        """Formats the tag as a VASP compliant INCAR instruction.
        
        Args:
            None
        
        Returns:
            str
        """
        comment = "! {}".format(self._comment)
        name = self._name.upper()  # ensure all upper 
        if type(self.value) is bool:
            if self.value:
                value = ".TRUE."
            else:
                value = ".FALSE."
        elif type(self.value) is np.ndarray:
            value = " ".join(self.value.astype(str))
        else:
            value = str(self.value)
        return "{}={}\t{}\n".format(name, value, comment)

    @property
    def value(self):
        """(object): Value of the tag."""
        return self._value

    @value.setter
    def value(self, v):
        valid = False
        for option in self._valid_options:
            if type(option) is type:
                if type(v) is option:
                    valid = True
            elif v == option:
                valid = True
        if valid:
            self._value = v
        else:
            raise ValueError()

#===============================#
#   VASP Tag Implementations    #
#===============================#

class AlgoTag(BaseTag):

    def __init__(self, value):
        comment = ("""Determines the electronic minimization algorithm and/or 
                   GW calculation type.""")
        name = "ALGO"
        valid_options = [
            "Normal", "VeryFast", "Fast", "Conjugate", "All", "Damped",
            "Subrot", "Eigenval", "Exact", "None", "Nothing", "CHI", "G0W0",
            "GW0", "GW", "scGW0", "scGW", "G0W0R", "GW0R", "GWR", "scGW0R",
            "scGWR", "ACFDT", "RPA", "ACFDTR", "RPAR", "BSE", "TDHF"
        ]
        super().__init__(comment, name, valid_options, value)


class EdiffTag(BaseTag):

    def __init__(self, value):
        comment = "The global break condition for the electronic SC-loop."
        name = "EDIFF"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class EdiffgTag(BaseTag):

    def __init__(self, value):
        comment = ("""Determines the break condition for the ionic relaxation 
                   loop.""")
        name = "EDIFFG"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class EncutTag(BaseTag):

    def __init__(self, value):
        comment = "Cutoff energy for the planewave basis set in eV."
        name = "ENCUT"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class IbrionTag(BaseTag):

    def __init__(self, value):
        comment = "Determines how the ions are updated and moved."
        name = "IBRION"
        valid_options = [-1, 0, 1, 2, 3, 5, 6, 7, 8, 44]
        super().__init__(comment, name, valid_options, value)


class IchargTag(BaseTag):

    def __init__(self, value):
        comment = "Determines construction of the initial charge density."
        name = "ICHARG"
        valid_options = [0, 1, 2, 4]
        super().__init__(comment, name, valid_options, value)


class IsifTag(BaseTag):

    def __init__(self, value):
        comment = ("""Determines whether the stress tensor is calculated and 
                   which degrees of freedom are allowed to change.""")
        name = "ISIF"
        valid_options = [0, 1, 2, 3, 4, 5, 6, 7]
        super().__init__(comment, name, valid_options, value)


class IsmearTag(BaseTag):

    def __init__(self, value):
        comment = "Determines how partial occupancies are set for each orbital."
        name = "ISMEAR"
        valid_options = [int]  # can be -5 -> any
        super().__init__(comment, name, valid_options, value)


class IspinTag(BaseTag):

    def __init__(self, value):
        comment = "Specifies spin polarization."
        name = "ISPIN"
        valid_options = [1, 2]
        super().__init__(comment, name, valid_options, value)


class IstartTag(BaseTag):

    def __init__(self, value):
        comment = "Determines whether or not to read the WAVECAR file."
        name = "ISTART"
        valid_options = [0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)


class IsymTag(BaseTag):

    def __init__(self, value):
        comment = "Determines how symmetry is treated."
        name = "ISYM"
        valid_options = [-1, 0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)


class LchargTag(BaseTag):

    def __init__(self, value):
        comment = "Determines whether or not a CHARGCAR/CHG file is written."
        name = "LCHARG"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class LrealTag(BaseTag):

    def __init__(self, value):
        comment = ("""Determines whether the projection operators are evaluated 
                   in real space or reciprocal space.""")
        name = "LREAL"
        valid_options = [bool, "On", "O", "Auto", "A"]
        super().__init__(comment, name, valid_options, value)


class LvtotTag(BaseTag):

    def __init__(self, value):
        comment = "Determines whether or not a LOCPOT file is written."
        name = "LVTOT"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class LwaveTag(BaseTag):

    def __init__(self, value):
        comment = "Determines whether or not a WAVECAR file is written."
        name = "LWAVE"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class MagmomTag(BaseTag):

    def __init__(self, value):
        comment = "Specifiec the initial magnetic moment for each atom."
        name = "MAGMOM"
        valid_options = [np.ndarray]
        super().__init__(comment, name, valid_options, value)


class NelmTag(BaseTag):

    def __init__(self, value):
        comment = "The maximum number of electronic SC steps."
        name = "NELM"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class NswTag(BaseTag):

    def __init__(self, value):
        comment = "Maximum number of ionic steps."
        name = "NSW"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class PotimTag(BaseTag):

    def __init__(self, value):
        comment = "Specifies the time step or step width scaling."
        name = "POTIM"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class PrecTag(BaseTag):

    def __init__(self, value):
        comment = "Determines the precision mode."
        name = "PREC"
        valid_options = [
            "Low", "Medium", "High", "Normal", "Single", "Accurate"
        ]
        super().__init__(comment, name, valid_options, value)


class SigmaTag(BaseTag):

    def __init__(self, value):
        comment = "The width of the smearing in eV."
        name = "SIGMA"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class SymprecTag(BaseTag):

    def __init__(self, value):
        comment = "Determines accuracy with which positions must be specified."
        name = "SYMPREC"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)
