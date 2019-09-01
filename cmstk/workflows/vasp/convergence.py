from cmstk.vasp.incar import IncarFile
from cmstk.vasp.incar_tags import EncutTag
from cmstk.vasp.kpoints import KpointsFile
from cmstk.vasp.poscar import PoscarFile
from cmstk.vasp.potcar import PotcarFile
from cmstk.workflows.vasp.base import VaspCalculation
import copy
import os
from typing import Any, List, Optional, Tuple


def converge_encut(calculation: VaspCalculation, encut_values: List[int],
                   working_directory: str) -> None:
    """Runs an ENCUT convergence calculation.

    Args:
        calculation: The VaspCalculation object to clone and converge.
        encut_values: The ENCUT values to test.
        working_directory: Path to the working directory.
    """
    # This needs work
    d = {encut: copy.deepcopy(calculation) for encut in encut_values}
    # setup directories
    for encut, calc in d.items():
        dirname = "{}eV".format(encut)
        calc_dir = os.path.join(working_directory, dirname)
        if not os.path.exists(calc_dir):
            os.makedirs(calc_dir)
        calc.calculation_directory = calc_dir
        if calc.incar is None:
            err = "Missing required input file (INCAR)."
            raise ValueError(err)
        tag_names = [name for name, _ in calc.incar.tags]
        if "ENCUT" in tag_names:
            calc.incar.tags["ENCUT"].value = encut
        else:
            calc.incar.tags.append(EncutTag(encut))
        calc.write()
        os.chdir(calc_dir)
        if calc.submission_script is None:
            err = "Missing required input file (submission script)."
            raise ValueError(err)
        path = os.path.join(calc_dir, "runjob.sh")
        cmd = "{} {}".format(calc.submission_script.exec_cmd, path)
        os.system(cmd)


def converge_kpoints(calculation: VaspCalculation,
                     kpoint_sizes: List[Tuple[int, int, int]],
                     working_directory: str) -> None:
    """Runs a KPOINTS convergence calculation.
    
    Args:
        calculation: The VaspCalculation object to clone and converge.
        kpoint_sizes: The KPOINTS mesh sizes to test.
        working_directory: Path to the working directory.
    """
    d = {
        kpoint_size: copy.deepcopy(calculation)
        for kpoint_size in kpoint_sizes
    }
    # setup directories
    for kpoint_size, calc in d.items():
        dirname = "{}x{}x{}".format(*kpoint_size)
        calc_dir = os.path.join(working_directory, dirname)
        if not os.path.exists(calc_dir):
            os.makedirs(calc_dir)
        calc.calculation_directory = calc_dir
        if calc.kpoints is None:
            err = "Missing required input file (KPOINTS)."
            raise ValueError(err)
        calc.kpoints.mesh_size = kpoint_size
        calc.write()
        os.chdir(calc_dir)
        if calc.submission_script is None:
            err = "Missing required input file (submission script)."
            raise ValueError(err)
        path = os.path.join(calc_dir, "runjob.sh")
        cmd = "{} {}".format(calc.submission_script.exec_cmd, path)
        os.system(cmd)
