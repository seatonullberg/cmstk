# ==================================================================== #
# Example of a verbose ENCUT convergence calculation automation script #
# ==================================================================== #

from cmstk.hpc.slurm import SubmissionScript
from cmstk.hpc.slurm_tags import *
from cmstk.structures.atoms import Atom
from cmstk.structures.crystals import Lattice
from cmstk.workflows.vasp.base import VaspCalculation
from cmstk.workflows.vasp.convergence import converge_encut
from cmstk.vasp.incar import IncarFile
from cmstk.vasp.incar_tags import *
from cmstk.vasp.kpoints import KpointsFile
from cmstk.vasp.poscar import PoscarFile
from cmstk.vasp.potcar import PotcarFile
import datetime
import os


working_directory = "YOUR/WORKING/DIRECTORY/HERE"
encut_values = [300, 350, 400, 450, 500, 550]

# Define the KPOINTS file
kpoints = KpointsFile(mesh_size=(12, 12, 12))

# Define the lattice structure in a POSCAR
a0 = 2.856
symbol = "Fe"
cm = np.array([[a0, 0, 0], [0, a0, 0], [0, 0, a0]])
atoms = [
    Atom(position=np.array([0, 0, 0]), symbol=symbol),
    Atom(position=np.array([a0/2, a0/2, a0/2]), symbol=symbol)
]
lattice = Lattice(atoms=atoms, coordinate_matrix=cm)
poscar = PoscarFile(lattice=lattice)

# Load in a POTCAR
# Multiple can be loaded together (variadic args)
path = os.path.join(working_directory, "POTCAR")
potcar = PotcarFile(path)
potcar.read()

# Define the INCAR file
incar_tags = [
    AlgoTag("Normal"),
    EdiffTag(1e-06),
    EdiffgTag(-0.001),
    IbrionTag(2),
    IchargTag(2),
    IsifTag(3),
    IsmearTag(0),
    IspinTag(2),
    IstartTag(0),
    LchargTag(False),
    LrealTag(False),
    LvtotTag(False),
    LwaveTag(False),
    NelmTag(40),
    NswTag(1),
    PrecTag("High"),
    SigmaTag(0.05),
    SystemTag("Fe BCC Unit")
]
# Tags can also be loaded from a json file with IncarFile.from_default()
incar = IncarFile(tags=incar_tags)

# Define the SubmissionScript
slurm_tags = [
    AccountTag("phillpot"),
    DistributionTag("cyclic:cyclic"),
    ErrorTag("job.err"),
    JobNameTag("converge_encut"),
    MemPerCpuTag(100),
    NtasksTag(16),
    OutputTag("job.out"),
    QosTag("phillpot"),
    TimeTag(datetime.timedelta(hours=1))
]
slurm_cmds = [
    "module load intel/2016.0.109",
    "module load impi/5.1.1",
    "srun --mpi=pmi2 $VASP_BIN > vasp.log"
]
submission_script = SubmissionScript(cmds=slurm_cmds, tags=slurm_tags)
calculation = VaspCalculation(
    incar=incar,
    kpoints=kpoints,
    poscar=poscar,
    potcar=potcar,
    submission_script=submission_script
)

# Finally, submit the series of jobs
# They will all run simultaneously barring local queue limits
converge_encut(calculation, encut_values, working_directory)
