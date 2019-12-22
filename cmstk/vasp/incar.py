from cmstk.filetypes import TextFile
from cmstk.util import BaseTag
from typing import Any, List, Optional


class IncarTag(BaseTag):
    """Tag preconfigured for INCAR files.
    
    Args:
        name: The tag's name.
        comment: Description of the tag's purpose.
        value: The value of the tag.
    
    Attributes:
        name: The tag's name.
        comment: Description of the tag's purpose.
        value: The value of the tag.
    """

    _comment_prefix = "!"
    _name_prefix = ""

    def __init__(self,
                 name: Optional[str] = None,
                 comment: Optional[str] = None,
                 value: Any = None) -> None:
        super().__init__(name, comment, value)


class IncarFile(TextFile):
    """File wrapper for a VASP INCAR file.

    Args:
        filepath: Filepath to an INCAR file
        tags: The VASP tags in the incar file.

    Attributes:
        filepath: Filepath to an INCAR file.
        tags: The VASP tags in the incar file.
    """

    def __init__(self,
                 filepath: Optional[str] = None,
                 tags: Optional[List[IncarTag]] = None) -> None:
        if filepath is None:
            filepath = "INCAR"
        self.filepath = filepath
        self._tags = tags

    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            for tag in self.tags:
                f.write("{}\n".format(tag.to_str()))

    @property
    def tags(self) -> List[IncarTag]:
        if self._tags is None:
            self._tags = []
            for line in self.lines:
                self._tags.append(IncarTag.from_str(line))  # type: ignore
        return self._tags

    @tags.setter
    def tags(self, value: List[IncarTag]) -> None:
        self._tags = value


class AlgoTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "ALGO",
            "Determines the electronic minimization algorithm and/or GW calculation type",
            value)


class AminTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "AMIN",
            "Minimal mixing parameter in Kerker's initial approximation to the charge dielectric function used in the Broyden/Pulay mixing scheme",
            value)


class AmixTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("AMIX", "Linear mixing parameter", value)


class AmixMagTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("AMIX_MAG",
                         "Linear mixing parameter for magnetization density",
                         value)


class BmixTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("BMIX",
                         "Cutoff wave vector for Kerker's mixing scheme", value)


class BmixMagTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "BMIX_MAG",
            "Cutoff wave vector for Kerker mixing scheme for the magnetization density",
            value)


class EdiffTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "EDIFF", "The global break condition for the electronic SC-loop",
            value)


class EdiffgTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "EDIFFG",
            "Determines the break condition for the ionic relaxation loop",
            value)


class EncutTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("ENCUT",
                         "Cutoff energy for the planewave basis set in eV",
                         value)


class IbrionTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("IBRION",
                         "Determines how the ions are updated and moved", value)


class IchargTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "ICHARG", "Determines construction of the initial charge density",
            value)


class IsifTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "ISIF",
            "Determines whether the stress tensor is calculated and which degrees of freedom are allowed to change",
            value)


class IsmearTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "ISMEAR",
            "Determines how partial occupancies are set for each orbital",
            value)


class IspinTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("ISPIN", "Specifies spin polarization", value)


class IstartTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("ISTART",
                         "Determines whether or not to read the WAVECAR file",
                         value)


class IsymTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("ISYM", "Determines how symmetry is treated", value)


class LchargTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "LCHARG",
            "Determines whether or not a CHARGCAR/CHG file is written", value)


class LorbitTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "LORBIT", "Determines whether PROCAR or PROUT files are written",
            value)


class LrealTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "LREAL",
            "Determines whether the projection operators are evaluated in real space or reciprocal space",
            value)


class LvtotTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("LVTOT",
                         "Determines whether or not a LOCPOT file is written",
                         value)


class LwaveTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("LWAVE",
                         "Determines whether or not a WAVECAR file is written",
                         value)


class MagmomTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("MAGMOM",
                         "Specifies the initial magnetic moment for each atom",
                         value)


class NcoreTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("NCORE",
                         "Determines the number of compute nodes per orbital",
                         value)


class NelmTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("NELM", "The maximum number of electronic SC steps",
                         value)


class NelminTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "NELMIN", "Specifies the minimum number of electronic SCF steps",
            value)


class NparTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("NPAR",
                         "Determines the number of bands treated in parallel",
                         value)


class NswTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("NSW", "Maximum number of ionic steps", value)


class PotimTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("POTIM",
                         "Specifies the time step or step width scaling", value)


class PrecTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("PREC", "Determines the precision mode", value)


class SigmaTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("SIGMA", "The width of the smearing in eV", value)


class SymprecTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "SYMPREC",
            "Determines accuracy with which positions must be specified", value)


class SystemTag(IncarTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("SYSTEM", "Description of the simulation", value)
