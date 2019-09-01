from cmstk.vasp.incar import IncarFile
from cmstk.vasp.incar_tags import EncutTag
from cmstk.vasp.kpoints import KpointsFile
from cmstk.vasp.poscar import PoscarFile
from cmstk.vasp.potcar import PotcarFile
from cmstk.workflows.vasp.base import VaspCalculation
import copy
import os
from typing import Any, List, Optional


def converge_encut(calculation: VaspCalculation,
                   encut_values: List[int],
                   working_directory: str) -> None:
    """Runs an ENCUT convergence calculation.

    Args:
        calculation: The VaspCalculation object to clone and converge.
        encut_values: The ENCUT values to test.
        working_directory: Path to the working directory.
    """
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

# TODO:
if False:
    def converge_kpoints(kpoint_sizes: List[List[int]],
                        incar: IncarFile,
                        kpoints: KpointsFile,
                        poscar: PoscarFile,
                        potcar: PotcarFile,
                        submission_script: Any,
                        working_directory: Optional[str] = None) -> None:
        """Runs a KPOINTS convergence calculation.
        
        Args:
            kpoint_sizes: The mesh sizes to test.
            incar: The INCAR file to use.
            kpoints: The KPOINTS file to use.
            - Any value of mesh_size will be overwritten
            poscar: The POSCAR file to use.
            potcar: The POTCAR file to use.
            submission_script: The job submission script to use.
            working_directory: The directory in which calculations are setup.
        """
        # setup directories
        if working_directory is None:
            working_directory = os.getcwd()
        calculation_directories = []
        for size in kpoint_sizes:
            dirname = "{}x{}x{}".format(*size)
            path = os.path.join(working_directory, dirname)
            if not os.path.exists(path):
                os.makedirs(path)
            calculation_directories.append(path)
        # iterate through each directory
        for i, calc_dir in enumerate(calculation_directories):
            # process KPOINTS
            mesh_size = kpoint_sizes[i]
            kpoints.mesh_size = mesh_size
            _submit_vasp_calculation(incar, kpoints, poscar, potcar, 
                                    submission_script, calc_dir)


    def _submit_vasp_calculation(incar: IncarFile, kpoints: KpointsFile,
                                poscar: PoscarFile, potcar: PotcarFile,
                                script: Any, calc_dir: str) -> None: # NEED ABSTRACT SubmissionScript
        incar.write(os.path.join(calc_dir, "INCAR"))
        kpoints.write(os.path.join(calc_dir, "KPOINTS"))
        poscar.write(os.path.join(calc_dir, "POSCAR"))
        potcar.write(os.path.join(calc_dir, "POTCAR"))
        path = os.path.join(calc_dir, "runjob.sh")
        script.write(os.path.join(calc_dir, path))
        os.chdir(calc_dir)
        cmd = "{} {}".format(script.exec_cmd, path)
        os.system(cmd)
