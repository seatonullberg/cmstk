from cmstk.hpc.slurm_tags import SlurmTag
from cmstk.utils import BaseTagCollection
from typing import Any, Optional, Sequence


class SubmissionScript(object):
    """File wrapper for a SLURM submission script.
    
    Args:
        filepath: Filepath to a SLURM script.
        cmds: Commands to execute after the #SBATCH specification.
        tags: The slurm tags to be included in the submission script.

    Attributes:
        filepath: Filepath to an INCAR file.

    Properties:
        cmds: Commands to execute after the #SBATCH specification.
        exec_cmd: The shell command used to execute this script.
        tags: Sequence of slurm tag objects which can be accessed like a dict.
    """
    def __init__(self,
                 filepath: Optional[str] = None,
                 cmds: Optional[Sequence[str]] = None,
                 tags: Optional[Sequence[Any]] = None) -> None:
        if filepath is None:
            filepath = "runjob.slurm"
        self.filepath = filepath
        if cmds is None:
            cmds = []
        self._cmds = cmds
        self._tags = BaseTagCollection(SlurmTag, tags)
        self._exec_cmd = "sbatch"

    def read(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
            lines = list(map(lambda x: x.strip(), lines))  # remove newlines
            lines = list(filter(None, lines))  # remove empty strings
        tags = self.tags.load_all_tags(base_class=SlurmTag,
                                       module_str="cmstk.hpc.slurm_tags")
        cmds = []
        for line in lines:
            if line.startswith("#!"):
                continue
            elif line.startswith("#SBATCH"):
                is_valid = False
                for tag in tags:
                    try:
                        tag.read(line)
                    except ValueError:
                        continue
                    else:
                        is_valid = True
                        self.tags.append(tag)
                        break
                if not is_valid:
                    err = "unable to parse the following line: {}".format(line)
                    raise ValueError(err)
            else:
                cmds.append(line)
        self._cmds = cmds

    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("#!/bin/bash\n")
            for _, tag in self.tags:
                f.write(tag.write())
            f.write("\n")
            for cmd in self.cmds:
                f.write("{}\n".format(cmd))

    @property
    def cmds(self) -> Sequence[str]:
        return self._cmds

    @property
    def exec_cmd(self) -> str:
        return self._exec_cmd

    @property
    def tags(self) -> BaseTagCollection:
        return self._tags
