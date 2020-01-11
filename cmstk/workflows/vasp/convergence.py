from cmstk.vasp.incar import IncarFile, EncutTag
from cmstk.vasp.kpoints import KpointsFile
from cmstk.vasp.poscar import PoscarFile
from cmstk.vasp.potcar import PotcarFile
from cmstk.hpc.util import BaseSubmissionScript
from cmstk.workflows.vasp.util import start_calculation, write_input_files
import os
from typing import List, Optional, Tuple


def converge_encut(
    encut_values: List[int],
    incar: IncarFile,
    kpoints: KpointsFile,
    poscar: PoscarFile,
    potcar: PotcarFile,
    submission_script: BaseSubmissionScript,
    calc_dir: Optional[str] = None,
) -> None:
    """Starts an ENCUT convergence calculation.

    Args:
        encut_values: The ENCUT values to test.
        incar: The vasp INCAR file.
        kpoints: The vasp KPOINTS file.
        poscar: The vasp POSCAR file.
        potcar: The vasp POTCAR file.
        submission_script: The hpc submission script.
        calc_dir: The directory in which to execute the calculation.
    """
    if calc_dir is None:
        calc_dir = os.getcwd()
    for encut in encut_values:
        new_tags = []
        has_encut = False
        for tag in incar.tags:
            if tag.name == "ENCUT":
                has_encut = True
                tag.value = encut
            new_tags.append(tag)
        if not has_encut:
            new_tags.append(EncutTag(encut))
        incar.tags = new_tags
        dirname = "{}eV".format(encut)
        path = os.path.join(calc_dir, dirname)
        if not os.path.exists(path):
            os.makedirs(path)
        write_input_files(path, incar, kpoints, poscar, potcar, submission_script)
        start_calculation(path, submission_script)


def converge_kpoints(
    kpoint_sizes: List[Tuple[int, int, int]],
    incar: IncarFile,
    kpoints: KpointsFile,
    poscar: PoscarFile,
    potcar: PotcarFile,
    submission_script: BaseSubmissionScript,
    calc_dir: Optional[str] = None,
) -> None:
    """Starts a KPOINTS convergence calculation.

    Args:
        kpoint_sizes: The KPOINT mesh sizes to test.
        incar: The vasp INCAR file.
        kpoints: The vasp KPOINTS file.
        poscar: The vasp POSCAR file.
        potcar: The vasp POTCAR file.
        submission_script: The hpc submission script.
        calc_dir: The directory in which to execute the calculation.
    """
    if calc_dir is None:
        calc_dir = os.getcwd()
    for ks in kpoint_sizes:
        kpoints.mesh_size = ks
        dirname = "{}x{}x{}".format(*ks)
        path = os.path.join(calc_dir, dirname)
        if not os.path.exists(path):
            os.makedirs(path)
        write_input_files(path, incar, kpoints, poscar, potcar, submission_script)
        start_calculation(path, submission_script)
