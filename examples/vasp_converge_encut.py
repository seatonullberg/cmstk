from ase.build import bulk
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


# Example of a verbose ENCUT convergence calculation automation script


working_directory = "YOUR/WORKING/DIRECTORY/HERE"  # replace with your working directory
encut_values = [300, 350, 400, 450, 500, 550]  # replace with the ENCUT values you want to test

# Define the KPOINTS file
kpoints = KpointsFile()
kpoints.mesh_size = (12, 12, 12)

# Define the underlying lattice structure
# ase for structure generation until it can be brought in-house
a0 = 2.856
ase_atoms = bulk(name="Fe", crystalstructure="bcc", a=a0, cubic=True)
lattice = Lattice(vectors=np.array(
    [[a0, 0, 0],
     [0, a0, 0],
     [0, 0, a0]]
))
for position in ase_atoms.positions:
    lattice.add_atom(Atom(position=position))
poscar = PoscarFile(
    direct=False,
    lattice=lattice,
    n_atoms_per_symbol=[2]
)

# Load in a POTCAR
path = os.path.join(working_directory, "POTCAR")  # Can load multiple POTCARS from anywhere
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
    NcoreTag(4),
    NelmTag(40),
    NswTag(40),
    PrecTag("High"),
    SigmaTag(0.05),
    SystemTag("Fe BCC Unit")
]
incar = IncarFile(tags=incar_tags)

# Define the SubmissionScript
# Replace these tag values with yours
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
# Replace these commands with yours
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
converge_encut(calculation, encut_values, working_directory)

