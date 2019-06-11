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
        self._valid_options = valid_options
        if value in None:
            self._value = value
        else:
            self.value = value  # do necessary checks on assignment

    def read_str(self, s, t):
        """Parses the value out of an INCAR line.
    
        Args:
            s (str): INCAR line.
            t (type): Return type

        Returns:
            instance of type t
        """
        s = s.split("=")
        # TODO: Take into account possible comment line 
        # this can fail for certain array representations
        s = s[1].split()[0].strip()
        if t is np.ndarray:
            raise NotImplementedError()
        elif t is bool:
            if s == ".TRUE.":
                return True
            elif s == ".FALSE.":
                return False
            else:
                raise ValueError()
        else:
            return t(s)

    def write_str(self):
        """Formats the tag as a VASP compliant INCAR instruction.

        Args:
            None

        Returns:
            str
        """
        t = type(self.value)
        if t is np.ndarray:
            s = " ".join(self.value.astype(str))
        elif t is bool:
            if self.value:
                s = ".TRUE."
            else:
                s = ".FALSE."
        else:
            s = str(self.value)
        return "{} = {}\t\t{}\n".format(self._name, s, self._comment)

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

    def __init__(self, value=None):
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

    def __init__(self, value=None):
        comment = "The global break condition for the electronic SC-loop."
        name = "EDIFF"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class EdiffgTag(BaseTag):

    def __init__(self, value=None):
        comment = ("""Determines the break condition for the ionic relaxation 
                   loop.""")
        name = "EDIFFG"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class EncutTag(BaseTag):

    def __init__(self, value=None):
        comment = "Cutoff energy for the planewave basis set in eV."
        name = "ENCUT"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class IbrionTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines how the ions are updated and moved."
        name = "IBRION"
        valid_options = [-1, 0, 1, 2, 3, 5, 6, 7, 8, 44]
        super().__init__(comment, name, valid_options, value)


class IchargTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines construction of the initial charge density."
        name = "ICHARG"
        valid_options = [0, 1, 2, 4]
        super().__init__(comment, name, valid_options, value)


class IsifTag(BaseTag):

    def __init__(self, value=None):
        comment = ("""Determines whether the stress tensor is calculated and 
                   which degrees of freedom are allowed to change.""")
        name = "ISIF"
        valid_options = [0, 1, 2, 3, 4, 5, 6, 7]
        super().__init__(comment, name, valid_options, value)


class IsmearTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines how partial occupancies are set for each orbital."
        name = "ISMEAR"
        valid_options = [int]  # can be -5 -> any
        super().__init__(comment, name, valid_options, value)


class IspinTag(BaseTag):

    def __init__(self, value=None):
        comment = "Specifies spin polarization."
        name = "ISPIN"
        valid_options = [1, 2]
        super().__init__(comment, name, valid_options, value)


class IstartTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines whether or not to read the WAVECAR file."
        name = "ISTART"
        valid_options = [0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)


class IsymTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines how symmetry is treated."
        name = "ISYM"
        valid_options = [-1, 0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)


class LchargTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a CHARGCAR/CHG file is written."
        name = "LCHARG"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class LrealTag(BaseTag):

    def __init__(self, value=None):
        comment = ("""Determines whether the projection operators are evaluated 
                   in real space or reciprocal space.""")
        name = "LREAL"
        valid_options = [bool, "On", "O", "Auto", "A"]
        super().__init__(comment, name, valid_options, value)


class LvtotTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a LOCPOT file is written."
        name = "LVTOT"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class LwaveTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a WAVECAR file is written."
        name = "LWAVE"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class MagmomTag(BaseTag):

    def __init__(self, value=None):
        comment = "Specifiec the initial magnetic moment for each atom."
        name = "MAGMOM"
        valid_options = [np.ndarray]
        super().__init__(comment, name, valid_options, value)


class NelmTag(BaseTag):

    def __init__(self, value=None):
        comment = "The maximum number of electronic SC steps."
        name = "NELM"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class NswTag(BaseTag):

    def __init__(self, value=None):
        comment = "Maximum number of ionic steps."
        name = "NSW"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class PotimTag(BaseTag):

    def __init__(self, value=None):
        comment = "Specifies the time step or step width scaling."
        name = "POTIM"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class PrecTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines the precision mode."
        name = "PREC"
        valid_options = [
            "Low", "Medium", "High", "Normal", "Single", "Accurate"
        ]
        super().__init__(comment, name, valid_options, value)


class SigmaTag(BaseTag):

    def __init__(self, value=None):
        comment = "The width of the smearing in eV."
        name = "SIGMA"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class SymprecTag(BaseTag):

    def __init__(self, value=None):
        comment = "Determines accuracy with which positions must be specified."
        name = "SYMPREC"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)
    