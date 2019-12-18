from cmstk.filetypes import TextFile
from cmstk.util import Tag
from typing import Any, List, Optional


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
                 tags: Optional[List[Tag]] = None) -> None:
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
    def tags(self) -> List[Tag]:
        if self._tags is None:
            self._tags = []
            for line in self.lines:
                self._tags.append(Tag.from_str(line))
        return self._tags

    @tags.setter
    def tags(self, value: List[Tag]) -> None:
        self._tags = value


def algo_tag(value: Any = None) -> Tag:
    return Tag(
        name="ALGO",
        comment=
        "Determines the electronic minimization algorithm and/or GW calculation type.",
        value=value)


def amin_tag(value: Any = None) -> Tag:
    return Tag(
        name="AMIN",
        comment=
        "Minimal mixing parameter in Kerker's initial approximation to the charge dielectric function used in the Broyden/Pulay mixing scheme.",
        value=value)


def amix_tag(value: Any = None) -> Tag:
    return Tag(name="AMIX", comment="Linear mixing parameter.", value=value)


def amix_mag_tag(value: Any = None) -> Tag:
    return Tag(name="AMIX_MAG",
               comment="Linear mixing parameter for magnetization density.",
               value=value)


def bmix_mag(value: Any = None) -> Tag:
    return Tag(name="BMIX",
               comment="Cutoff wave vector for Kerker mixing scheme.",
               value=value)


def bmix_mag_tag(value: Any = None) -> Tag:
    return Tag(
        name="BMIX_MAG",
        comment=
        "Cutoff wave vector for Kerker mixing scheme for the magnetization density.",
        value=value)


def ediff_tag(value: Any = None) -> Tag:
    return Tag(name="EDIFF",
               comment="The global break condition for the electronic SC-loop",
               value=value)


def ediffg_tag(value: Any = None) -> Tag:
    return Tag(
        name="EDIFFG",
        comment="Determines the break condition for the ionic relaxation loop.",
        value=value)


def encut_tag(value: Any = None) -> Tag:
    return Tag(name="ENCUT",
               comment="Cutoff energy for the planewave basis set in eV.",
               value=value)


def ibrion_tag(value: Any = None) -> Tag:
    return Tag(name="IBRION",
               comment="Determines how the ions are updated and moved.",
               value=value)


def icharg_tag(value: Any = None) -> Tag:
    return Tag(name="ICHARG",
               comment="Determines construction of the initial charge density.",
               value=value)


def isif_tag(value: Any = None) -> Tag:
    return Tag(
        name="ISIF",
        comment=
        "Determines whether the stress tensor is calculated and which degrees of freedom are allowed to change.",
        value=value)


def ismear_tag(value: Any = None) -> Tag:
    return Tag(
        name="ISMEAR",
        comment="Determines how partial occupancies are set for each orbital.",
        value=value)


def ispin_tag(value: Any = None) -> Tag:
    return Tag(name="ISPIN",
               comment="Specifies spin polarization.",
               value=value)


def istart_tag(value: Any = None) -> Tag:
    return Tag(name="ISTART",
               comment="Determines whether or not to read the WAVECAR file.",
               value=value)


def isym_tag(value: Any = None) -> Tag:
    return Tag(name="ISYM",
               comment="Determines how symmetry is treated.",
               value=value)


def lcharg_tag(value: Any = None) -> Tag:
    return Tag(
        name="LCHARG",
        comment="Determines whether or not a CHARGCAR/CHG file is writen.",
        value=value)


def lorbit_tag(value: Any = None) -> Tag:
    return Tag(name="LORBIT",
               comment="Determines whether PROCAR or PROOUT files are written.",
               value=value)


def lreal_tag(value: Any = None) -> Tag:
    return Tag(
        name="LREAL",
        comment=
        "Determines whether the projection operators are evaluated in real space or reciprocal space.",
        value=value)


def lvtot_tag(value: Any = None) -> Tag:
    return Tag(name="LVTOT",
               comment="Determines whether or not a LOCPOT file is written.",
               value=value)


def lwave_tag(value: Any = None) -> Tag:
    return Tag(name="LWAVE",
               comment="Determines whether or not a WAVECAR file is written.",
               value=value)


def magmom_tag(value: Any = None) -> Tag:
    return Tag(name="MAGMOM",
               comment="Specifies the initial magnetic moment for each atom.",
               value=value)


def ncore_tag(value: Any = None) -> Tag:
    return Tag(name="NCORE",
               comment="Determines the number of compute nodes per orbital.",
               value=value)


def nelm_tag(value: Any = None) -> Tag:
    return Tag(name="NELM",
               comment="The maximum number of electronic SC steps.",
               value=value)


def nelmin_tag(value: Any = None) -> Tag:
    return Tag(name="NELMIN",
               comment="Specifies the minimum number of electronic SCF steps.",
               value=value)


def npar_tag(value: Any = None) -> Tag:
    return Tag(name="NPAR",
               comment="Determines the number of bands treated in parallel.",
               value=value)


def nsw_tag(value: Any = None) -> Tag:
    return Tag(name="NSW",
               comment="Maxuimum number of ionic steps.",
               value=value)


def potim_tag(value: Any = None) -> Tag:
    return Tag(name="POTIM",
               comment="Specifies the time step or step width scaling.",
               value=value)


def prec_tag(value: Any = None) -> Tag:
    return Tag(name="PREC",
               comment="Determines the precision mode.",
               value=value)


def sigma_tag(value: Any = None) -> Tag:
    return Tag(name="SIGMA",
               comment="The width of the smearing in eV.",
               value=value)


def symprec_tag(value: Any = None) -> Tag:
    return Tag(
        name="SYMPREC",
        comment="Determines accuracy with which positions must be specified.",
        value=value)


def system_tag(value: Any = None) -> Tag:
    return Tag(name="SYSTEM",
               comment="Description of the simulation.",
               value=value)
