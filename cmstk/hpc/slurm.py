from cmstk.hpc.base import BaseScript
from cmstk.util import Tag
from typing import Any, List, Optional


class SlurmScript(BaseScript):
    """File wrapper for a SLURM submission script.

    Args:
        filepath: Filepath to a SLURM script.
        cmds: Commands to execute after the #SBATCH specification.
        tags: The slurm tags to be included in the submission script.

    Attributes:
        filepath: Filepath to a SLURM script.
        cmds: Commands to execute after the #SBATCH specification.
        exec_cmd: The shell command used to execute this script.
        tags: TagCollection which can be accessed like a dict.
    """

    def __init__(self,
                 filepath: Optional[str] = None,
                 cmds: Optional[List[str]] = None,
                 tags: Optional[List[Tag]] = None) -> None:
        if filepath is None:
            filepath = "runjob.slurm"
        exec_cmd = "sbatch"
        prefix = "#SBATCH"
        super().__init__(filepath, exec_cmd, prefix, cmds, tags)


def account_tag(value: Any = None) -> Tag:
    return Tag(name="--account",
               comment="user account name",
               prefix="#SBATCH",
               value=value)


def distribution_tag(value: Any = None) -> Tag:
    return Tag(name="--distribution",
               comment="distribution method for remote processes",
               prefix="#SBATCH",
               value=value)


def error_tag(value: Any = None) -> Tag:
    return Tag(name="--error",
               comment="filename to write stderr to",
               prefix="#SBATCH",
               value=value)


def job_name_tag(value: Any = None) -> Tag:
    return Tag(name="--job-name",
               comment="name of the job",
               prefix="#SBATCH",
               value=value)


def mail_type_tag(value: Any = None) -> Tag:
    return Tag(name="--mail-type",
               comment="email event triggers",
               prefix="#SBATCH",
               value=value)


def mail_user_tag(value: Any = None) -> Tag:
    return Tag(name="--mail-user",
               comment="user email address",
               prefix="#SBATCH",
               value=value)


def mem_per_cpu_tag(value: Any = None) -> Tag:
    return Tag(name="--mem-per-cpu",
               comment="memory to assign to each CPU",
               prefix="#SBATCH",
               value=value)


def ntasks_tag(value: Any = None) -> Tag:
    return Tag(name="--ntasks",
               comment="number of tasks to run",
               prefix="#SBATCH",
               value=value)


def output_tag(value: Any = None) -> Tag:
    return Tag(name="--output",
               comment="filename ot write stdout to",
               prefix="#SBATCH",
               value=value)


def qos_tag(value: Any = None) -> Tag:
    return Tag(name="--qos",
               comment="QOS account name",
               prefix="#SBATCH",
               value=value)


def time_tag(value: Any = None) -> Tag:
    return Tag(name="--time",
               comment="max duration of the job",
               prefix="#SBATCH",
               value=value)
