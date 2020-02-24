from cmstk.hpc.util import BaseSubmissionScript
from cmstk.util import BaseTag
from typing import Any, List, Optional


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

    @classmethod
    def from_str(cls, s: str) -> 'SlurmTag':
        # expected format: #SBATCH {name}={value} # {comment}
        parts = s.split("=")
        name = parts[0].split()[1]
        if "#" in parts[1]:
            value = parts[1].split("#")[0].strip()
            comment = parts[1].split("#")[1].strip()
        else:
            value = parts[1].strip()
            comment = ""
        return cls(name, comment, value)

    def __str__(self) -> str:
        return "#SBATCH {}={}\t{}".format(self.name, self.value, self.comment)


class SlurmSubmissionScript(BaseSubmissionScript):
    """File wrapper for a SLURM submission script.

    Args:
        filepath: Filepath to a SLURM script.
        cmds: Commands to execute after the #SBATCH specification.
        tags: The slurm tags to be included in the submission script.
        shebang: The shell specific shebang symbol.

    Attributes:
        filepath: Filepath to a SLURM script.
        cmds: Commands to execute after the #SBATCH specification.
        exec_cmd: The shell command used to execute this script.
        tags: TagCollection which can be accessed like a dict.
        shebang: The shell specific shebang symbol.
    """

    def __init__(self,
                 filepath: Optional[str] = None,
                 cmds: Optional[List[str]] = None,
                 tags: Optional[List[SlurmTag]] = None,
                 shebang: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "runjob.slurm"
        super().__init__(filepath, cmds, tags, shebang)

    @property
    def cmds(self) -> List[str]:
        if self._cmds is None:
            self._cmds = []
            for line in self.lines:
                line = line.strip()
                if line != self.shebang and not line.startswith("#SBATCH"):
                    self._cmds.append(line)
        return self._cmds

    @cmds.setter
    def cmds(self, value: List[str]) -> None:
        self._cmds = value

    @property
    def exec_cmd(self) -> str:
        return "sbatch"

    @property
    def tags(self) -> List[SlurmTag]:
        if self._tags is None:
            self._tags = []
            for line in self.lines:
                if line.startswith("#SBATCH"):
                    self._tags.append(SlurmTag.from_str(line))
        return self._tags

    @tags.setter
    def tags(self, value: List[SlurmTag]) -> None:
        self._tags = value


class AccountTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--account", "user account name", value)


class DistributionTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--distribution",
                         "distribution method for remote processes", value)


class ErrorTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--error", "filename to write stderr to", value)


class JobNameTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--job-name", "name of the job", value)


class MailTypeTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--mail-type", "email event triggers", value)


class MailUserTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--mail-user", "user email address", value)


class MemPerCpuTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--mem-per-cpu", "memory to assign to each CPU", value)


class NtasksTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--ntasks", "number of tasks to run", value)


class OutputTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--output", "filename to write stdout to", value)


class QosTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--qos", "QOS account name", value)


class TimeTag(SlurmTag):

    def __init__(self, value: Any = None) -> None:
        super().__init__("--time", "max duration of the job", value)
