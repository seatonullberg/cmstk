from cmstk.utils import BaseTag
import numpy as np
from typing import Any, Optional, Sequence


class VaspTag(BaseTag):
    """Representation of a generic INCAR tag.
    
    Args:
        comment: Description of the tag.
        name: VASP compliant tag name.
        valid_options: The values this tag accepts.
        value: Value assigned to the tag.
    """

    def __init__(self, comment: str, name: str, 
                 valid_options: Sequence[Any],
                 value: Optional[Any] = None) -> None:
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str) -> None:
        """Reads in tag info from a single line of text.
        
        Args:
            line: The string to parse.

        Returns:
            None
        
        Raises:
            ValueError:
            - If the parsed name does not match the tag's name
        """
        name = line.split()[0]
        if name != self.name:
            err = ("tag with name `{}` cannot be parsed by {}"
                   .format(name, self.__class__.__name__))
            raise ValueError(err)
        value = line.split()[2]
        self.value = value
        if "!" in line:
            comment = line.split("!")[1].strip()
            self.comment = comment 

    def write(self) -> str:
        """Writes a single line string from the tag info.
        
        Args:
            None

        Returns:
            None

        Raises:
            ValueError
            - If `value` is None
        """
        if self.value is None:
            err = "None value cannot be written."
            raise ValueError(err)
        s = "{} = {}\t! {}".format(self.name, self.value, self.comment)
        return s

#===============================#
#   VASP Tag Implementations    #
#===============================#

class AlgoTag(VaspTag):

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


class EdiffTag(VaspTag):

    def __init__(self, value=None):
        comment = "The global break condition for the electronic SC-loop."
        name = "EDIFF"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class EdiffgTag(VaspTag):

    def __init__(self, value=None):
        comment = ("""Determines the break condition for the ionic relaxation 
                   loop.""")
        name = "EDIFFG"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class EncutTag(VaspTag):

    def __init__(self, value=None):
        comment = "Cutoff energy for the planewave basis set in eV."
        name = "ENCUT"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class IbrionTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines how the ions are updated and moved."
        name = "IBRION"
        valid_options = [-1, 0, 1, 2, 3, 5, 6, 7, 8, 44]
        super().__init__(comment, name, valid_options, value)


class IchargTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines construction of the initial charge density."
        name = "ICHARG"
        valid_options = [0, 1, 2, 4]
        super().__init__(comment, name, valid_options, value)


class IsifTag(VaspTag):

    def __init__(self, value=None):
        comment = ("""Determines whether the stress tensor is calculated and 
                   which degrees of freedom are allowed to change.""")
        name = "ISIF"
        valid_options = [0, 1, 2, 3, 4, 5, 6, 7]
        super().__init__(comment, name, valid_options, value)


class IsmearTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines how partial occupancies are set for each orbital."
        name = "ISMEAR"
        valid_options = [int]  # can be -5 -> any
        super().__init__(comment, name, valid_options, value)


class IspinTag(VaspTag):

    def __init__(self, value=None):
        comment = "Specifies spin polarization."
        name = "ISPIN"
        valid_options = [1, 2]
        super().__init__(comment, name, valid_options, value)


class IstartTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not to read the WAVECAR file."
        name = "ISTART"
        valid_options = [0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)


class IsymTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines how symmetry is treated."
        name = "ISYM"
        valid_options = [-1, 0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)


class LchargTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a CHARGCAR/CHG file is written."
        name = "LCHARG"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class LrealTag(VaspTag):

    def __init__(self, value=None):
        comment = ("""Determines whether the projection operators are evaluated 
                   in real space or reciprocal space.""")
        name = "LREAL"
        valid_options = [bool, "On", "O", "Auto", "A"]
        super().__init__(comment, name, valid_options, value)


class LvtotTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a LOCPOT file is written."
        name = "LVTOT"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class LwaveTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a WAVECAR file is written."
        name = "LWAVE"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)


class MagmomTag(VaspTag):

    def __init__(self, value=None):
        comment = "Specifiec the initial magnetic moment for each atom."
        name = "MAGMOM"
        valid_options = [np.ndarray]
        super().__init__(comment, name, valid_options, value)


class NelmTag(VaspTag):

    def __init__(self, value=None):
        comment = "The maximum number of electronic SC steps."
        name = "NELM"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class NswTag(VaspTag):

    def __init__(self, value=None):
        comment = "Maximum number of ionic steps."
        name = "NSW"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)


class PotimTag(VaspTag):

    def __init__(self, value=None):
        comment = "Specifies the time step or step width scaling."
        name = "POTIM"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class PrecTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines the precision mode."
        name = "PREC"
        valid_options = [
            "Low", "Medium", "High", "Normal", "Single", "Accurate"
        ]
        super().__init__(comment, name, valid_options, value)


class SigmaTag(VaspTag):

    def __init__(self, value=None):
        comment = "The width of the smearing in eV."
        name = "SIGMA"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)


class SymprecTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines accuracy with which positions must be specified."
        name = "SYMPREC"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)
    