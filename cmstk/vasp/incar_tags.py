from cmstk.utils import BaseTag
import numpy as np
import re
from typing import Any, Optional, Sequence, Tuple


class VaspTag(BaseTag):
    """Representation of a generic INCAR tag.
    
    Args:
        name: VASP compliant tag name.
        valid_options: The values this tag accepts.
        comment: Description of the tag.
        value: Value assigned to the tag.
    """

    def __init__(self, name: str, 
                 valid_options: Sequence[Any],
                 comment: Optional[str] = None, 
                 value: Optional[Any] = None) -> None:
        super().__init__(name, valid_options, comment, value)

    def _read_array(self, line: str) -> None:
        """Reads in tag content with value interpreted as array.
        
        Notes:
            This implementation only works on the fully expanded array notation.

        Args:
            line: The string to parse.

        Returns:
            None
        """
        value, self.comment = self._read(line)
        self.value = np.array([float(x) for x in value.split()])

    def _read_bool(self, line: str) -> None:
        """Reads in tag content with value interpreted as bool.
        
        Args:
            line: The string to parse.

        Returns:
            None

        Raises:
            ValueError
            - If value cannot be interpreted
        """
        value, self.comment = self._read(line)
        if value == ".TRUE.":
            self.value = True
        elif value == ".FALSE.":
            self.value = False
        else:
            err = "unable to interpret `{}` as a bool type".format(value)
            raise ValueError(err)

    def _read_float(self, line: str) -> None:
        """Reads in tag content with value interpreted as float.
        
        Args:
            line: The string to parse.

        Returns:
            None
        """
        value, self.comment = self._read(line)
        self.value = float(value)

    def _read_int(self, line: str) -> None:
        """Reads in tag content with value interpreted as int.
        
        Args:
            line: The string to parse.

        Returns:
            None
        """
        value, self.comment = self._read(line)
        self.value = int(value)

    def _read_str(self, line: str) -> None:
        """Reads in tag content with value interpreted as str.
        
        Args:
            line: The string to read.

        Returns:
            None
        """
        self.value, self.comment = self._read(line)

    def _read(self, line: str) -> Tuple[str, Optional[str]]:
        """Reads raw tag content from a line of text.
        
        Args:
            line: The string to parse.

        Returns:
            Tuple[str, str]
            - The raw value and comment

        Raises:
            ValueError:
            - if the parsed name does not match the tag's name
            - If no value is found
        """
        name = line.split()[0]
        if name != self.name:
            err = ("tag with name `{}` cannot be parsed by {}"
                   .format(name, self.__class__))
            raise ValueError(err)
        comment: Optional[str]
        if "!" in line:
            # value is whatever is between `= ` and ` !`
            search_result = re.search("= (.*) !", line)
            if search_result is None:
                err = "unable to find value in line: {}".format(line)
                raise ValueError(err)
            else:
                value = search_result.group(1).strip()
                comment = line.split("!")[1].strip()
        else:
            value = line.split()[2]
            comment = None
        return (value, comment)

    def _write_array(self) -> str:
        """Writes a line of tag info with value interpreted as array.
        
        Args:
            None
        
        Returns:
            str
        """
        str_value = " ".join(str(x) for x in self.value)
        return self._write(str_value)

    def _write_bool(self) -> str:
        """Writes a line of tag info with value interpreted as bool.
        
        Notes:
            If value is None this will write False.

        Args:
            None

        Returns:
            str
        """
        if self.value:
            str_value = ".TRUE."
        else:
            str_value = ".FALSE."
        return self._write(str_value)

    def _write_float(self) -> str:
        """Writes a line of tag info with the value interpreted as float.

        Args:
            None

        Returns:
            str
        """
        str_value = "{:10.4f}".format(self.value)
        return self._write(str_value)

    def _write_int(self) -> str:
        """Writes a line of tag info with the value interpreted as int.
        
        Args:
            None

        Returns:
            str
        """
        str_value = str(self.value)
        return self._write(str_value)

    def _write_str(self) -> str:
        """Writes a line of tag info with the value interpreted as str.
        
        Args:
            None

        Returns:
            str
        """
        return self._write(self.value)

    def _write(self, str_value: str) -> str:
        """Writes a single line string from preprocessed tag info.
        
        Args:
            str_value: The tag's value formatted as VASP compliant text.

        Returns:
            str
        
        Raises:
            ValueError
            - If `str_value` is ""
        """
        if str_value == "":
            err = "writing a None value may have unforseen consequences"
            raise ValueError(err)
        s = "{} = {}\t! {}\n".format(self.name, str_value, self.comment)
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

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class EdiffTag(VaspTag):

    def __init__(self, value=None):
        comment = "The global break condition for the electronic SC-loop."
        name = "EDIFF"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_float(line)

    def write(self):
        return self._write_float()


class EdiffgTag(VaspTag):

    def __init__(self, value=None):
        comment = ("""Determines the break condition for the ionic relaxation 
                   loop.""")
        name = "EDIFFG"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_float(line)

    def write(self):
        return self._write_float()


class EncutTag(VaspTag):

    def __init__(self, value=None):
        comment = "Cutoff energy for the planewave basis set in eV."
        name = "ENCUT"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class IbrionTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines how the ions are updated and moved."
        name = "IBRION"
        valid_options = [-1, 0, 1, 2, 3, 5, 6, 7, 8, 44]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class IchargTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines construction of the initial charge density."
        name = "ICHARG"
        valid_options = [0, 1, 2, 4]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class IsifTag(VaspTag):

    def __init__(self, value=None):
        comment = ("""Determines whether the stress tensor is calculated and 
                   which degrees of freedom are allowed to change.""")
        name = "ISIF"
        valid_options = [0, 1, 2, 3, 4, 5, 6, 7]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class IsmearTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines how partial occupancies are set for each orbital."
        name = "ISMEAR"
        valid_options = [int]  # can be -5 -> any
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def writr(self):
        return self._write_int()


class IspinTag(VaspTag):

    def __init__(self, value=None):
        comment = "Specifies spin polarization."
        name = "ISPIN"
        valid_options = [1, 2]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class IstartTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not to read the WAVECAR file."
        name = "ISTART"
        valid_options = [0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class IsymTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines how symmetry is treated."
        name = "ISYM"
        valid_options = [-1, 0, 1, 2, 3]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class LchargTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a CHARGCAR/CHG file is written."
        name = "LCHARG"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_bool(line)

    def write(self):
        return self._write_bool()


class LrealTag(VaspTag):

    def __init__(self, value=None):
        comment = ("""Determines whether the projection operators are evaluated 
                   in real space or reciprocal space.""")
        name = "LREAL"
        valid_options = [bool, "On", "O", "Auto", "A"]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        try:
            self._read_bool(line)
        except ValueError:
            self._read_str(line)

    def write(self):
        if type(self.value) is bool:
            self._write_bool()
        else:
            self._write_str()


class LvtotTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a LOCPOT file is written."
        name = "LVTOT"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_bool(line)

    def write(self):
        return self._write_bool()


class LwaveTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines whether or not a WAVECAR file is written."
        name = "LWAVE"
        valid_options = [bool]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_bool(line)

    def write(self):
        return self._write_bool()


class MagmomTag(VaspTag):

    def __init__(self, value=None):
        comment = "Specifiec the initial magnetic moment for each atom."
        name = "MAGMOM"
        valid_options = [np.ndarray]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_array(line)

    def write(self):
        return self._write_array()


class NelmTag(VaspTag):

    def __init__(self, value=None):
        comment = "The maximum number of electronic SC steps."
        name = "NELM"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class NswTag(VaspTag):

    def __init__(self, value=None):
        comment = "Maximum number of ionic steps."
        name = "NSW"
        valid_options = [int]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()

class PotimTag(VaspTag):

    def __init__(self, value=None):
        comment = "Specifies the time step or step width scaling."
        name = "POTIM"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_float(line)

    def write(self):
        return self._write_float()


class PrecTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines the precision mode."
        name = "PREC"
        valid_options = [
            "Low", "Medium", "High", "Normal", "Single", "Accurate"
        ]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class SigmaTag(VaspTag):

    def __init__(self, value=None):
        comment = "The width of the smearing in eV."
        name = "SIGMA"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_float(line)

    def write(self):
        return self._write_float()


class SymprecTag(VaspTag):

    def __init__(self, value=None):
        comment = "Determines accuracy with which positions must be specified."
        name = "SYMPREC"
        valid_options = [float]
        super().__init__(comment, name, valid_options, value)

    def read(self, line: str):
        return self._read_float(line)

    def write(self):
        return self._write_float()
