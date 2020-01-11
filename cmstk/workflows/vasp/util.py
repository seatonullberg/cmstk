from cmstk.hpc.util import BaseSubmissionScript
from cmstk.vasp.incar import IncarFile
from cmstk.vasp.kpoints import KpointsFile
from cmstk.vasp.poscar import PoscarFile
from cmstk.vasp.potcar import PotcarFile
import os


def write_input_files(
    path: str,
    incar: IncarFile,
    kpoints: KpointsFile,
    poscar: PoscarFile,
    potcar: PotcarFile,
    submission_script: BaseSubmissionScript,
) -> None:
    for f in [incar, kpoints, poscar, potcar, submission_script]:
        filepath = os.path.join(path, f.filepath)
        f.write(filepath) # type: ignore


def start_calculation(path: str,
                      submission_script: BaseSubmissionScript) -> None:
    path = os.path.join(path, submission_script.filepath)
    cmd = "{} {}".format(submission_script.exec_cmd, path)
    os.system(cmd)
