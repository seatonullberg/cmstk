from cmstk.hpc.util import SubmissionScript
from cmstk.util import BaseTag
from typing import Any, List, Optional


class SlurmScript(SubmissionScript):
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
                 tags: Optional[List[BaseTag]] = None) -> None:
        if filepath is None:
            filepath = "runjob.slurm"
        exec_cmd = "sbatch"
        super().__init__(filepath, exec_cmd, cmds, tags)


class SlurmTag(BaseTag):
    """Tag preconfigured for SLURM inputs.
    
    Args:
        name: The tag's name.
        comment: Description of the tag's purpose.
        value: The value of the tag.

    Attributes:
        name: The tag's name.
        comment: Description of the tag's purpose.
        value: The value of the tag.
    """
    
    def __init__(self, 
                 name: Optional[str] = None, 
                 comment: Optional[str] = None,
                 value: Any = None) -> None:
        super().__init__(name, comment, value)


class AccountTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--account",
            "user account name",
            value)


class DistributionTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--distribution",
            "distribution method for remote processes",
            value)


class ErrorTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--error",
            "filename to write stderr to",
            value)


class JobNameTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--job-name",
            "name of the job",
            value)


class MailTypeTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--mail-type",
            "email event triggers",
            value)


class MailUserTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--mail-user",
            "user email address",
            value)


class MemPerCpuTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--mem-per-cpu",
            "memory to assign to each CPU",
            value)


class NtasksTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--ntasks",
            "number of tasks to run",
            value)


class OutputTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--output",
            "filename to write stdout to",
            value)


class QosTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--qos",
            "QOS account name",
            value)


class TimeTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__(
            "--time",
            "max duration of the job",
            value)
