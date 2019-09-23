from cmstk.vasp.incar import IncarFile
from cmstk.vasp.kpoints import KpointsFile
from cmstk.vasp.oszicar import OszicarFile
from cmstk.vasp.outcar import OutcarFile
from cmstk.vasp.poscar import PoscarFile
from cmstk.vasp.potcar import PotcarFile
import os
from typing import Any, Optional


class VaspCalculation(object):
    """Representation of a generic VASP calculation.
    
    Args:
        calculation_directory: Path to the calculation directory.
        incar: VASP IncarFile.
        kpoints: VASP KpointsFile.
        poscar: VASP PoscarFile.
        potcar: VASP PotcarFile.
        submission_script: HPC SubmissionScript.

    Attributes:
        calculation_directory: Path to the calculation directory.
        incar: VASP IncarFile.
        kpoints: VASP KpointsFile.
        oszicar: VASP OszicarFile.
        outcar: VASP OutcarFile.
        poscar: VASP PoscarFile.
        potcar: VASP PotcarFile.
        submission_script: HPC SubmissionScript.
    """
    def __init__(self,
                 calculation_directory: Optional[str] = None,
                 incar: Optional[IncarFile] = None,
                 kpoints: Optional[KpointsFile] = None,
                 poscar: Optional[PoscarFile] = None,
                 potcar: Optional[PotcarFile] = None,
                 submission_script: Optional[Any] = None) -> None:
        self.calculation_directory = calculation_directory
        self.incar = incar
        self.kpoints = kpoints
        self.oszicar: Optional[OszicarFile] = None
        self.outcar: Optional[OutcarFile] = None
        self.poscar = poscar
        self.potcar = potcar
        self.submission_script = submission_script

    def read(self, calculation_directory: Optional[str] = None) -> None:
        """Reads all of the VASP files in a given calculation directory.
        
        Args:
            calculation_directory: Path to the calculation directory.
        
        Raises:
            ValueError:
            - Cannot read without a path to the calculation directory.
        """
        if calculation_directory is None:
            calculation_directory = self.calculation_directory
        if calculation_directory is None:
            err = "Cannot read without a path to the calculation directory."
            raise ValueError(err)
        # read incar
        path = os.path.join(calculation_directory, "INCAR")
        if self.incar is None:
            self.incar = IncarFile()
        self.incar.read(path)
        # read kpoints
        path = os.path.join(calculation_directory, "KPOINTS")
        if self.kpoints is None:
            self.kpoints = KpointsFile()
        self.kpoints.read(path)
        # read oszicar
        path = os.path.join(calculation_directory, "OSZICAR")
        if self.oszicar is None:
            self.oszicar = OszicarFile()
        self.oszicar.read(path)
        # read outcar (OUTCAR does not follow read/write interface)
        # path = os.path.join(calculation_directory, "OUTCAR")
        # if self.outcar is None:
        #    self.outcar = OutcarFile()
        # self.outcar.read(path)
        # read poscar
        path = os.path.join(calculation_directory, "POSCAR")
        if self.poscar is None:
            self.poscar = PoscarFile()
        self.poscar.read(path)
        # read potcar
        path = os.path.join(calculation_directory, "POTCAR")
        if self.potcar is None:
            self.potcar = PotcarFile()
        self.potcar.read(path)

    def write(self, calculation_directory: Optional[str] = None) -> None:
        """Writes all necessary files to run a VASP calculation.
        
        Args:
            calculation_directory: Path to the calculation directory.

        Raises:
            ValueError:
            - Cannot write without a path to the calculation directory.
            - Missing a required input file.
        """
        if calculation_directory is None:
            calculation_directory = self.calculation_directory
        if calculation_directory is None:
            err = "Cannot write without a path to the calculation directory."
            raise ValueError(err)
        # write incar
        path = os.path.join(calculation_directory, "INCAR")
        if self.incar is None:
            err = "Missing a required input file (INCAR)."
            raise ValueError(err)
        self.incar.write(path)
        # write kpoints
        path = os.path.join(calculation_directory, "KPOINTS")
        if self.kpoints is None:
            err = "Missing a required input file (KPOINTS)."
            raise ValueError(err)
        self.kpoints.write(path)
        # write poscar
        path = os.path.join(calculation_directory, "POSCAR")
        if self.poscar is None:
            err = "Missing a required input file (POSCAR)."
            raise ValueError(err)
        self.poscar.write(path)
        # write potcar
        path = os.path.join(calculation_directory, "POTCAR")
        if self.potcar is None:
            err = "Missing a required input file (POTCAR)."
            raise ValueError(err)
        self.potcar.write(path)
        # write submission script
        path = os.path.join(calculation_directory, "runjob.sh")
        if self.submission_script is None:
            err = "Missing a required input file (submission script)."
            raise ValueError(err)
        self.submission_script.write(path)
