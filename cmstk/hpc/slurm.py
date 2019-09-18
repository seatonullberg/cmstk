from cmstk.hpc.slurm_tags import SlurmTag
from cmstk.utils import BaseTag, TagCollection
import os
from typing import List, Optional


class SubmissionScript(object):
    """File wrapper for a SLURM submission script.
    
    Args:
        filepath: Filepath to a SLURM script.
        cmds: Commands to execute after the #SBATCH specification.
        tags: The slurm tags to be included in the submission script.

    Attributes:
        filepath: Filepath to an INCAR file.
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
        self.filepath = filepath
        if cmds is None:
            cmds = []
        self._cmds = cmds
        self._tags = TagCollection(SlurmTag, tags)
        self._exec_cmd = "sbatch"

    def read(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
            lines = list(map(lambda x: x.strip(), lines))  # remove newlines
            lines = list(filter(None, lines))  # remove empty strings
        tags = self.tags.import_tags(common_class=SlurmTag,
                                     module="cmstk.hpc.slurm_tags")
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
                        self.tags.insert(tag)
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
            for tag in self.tags.values():
                f.write(tag.write())
            f.write("\n")
            for cmd in self.cmds:
                f.write("{}\n".format(cmd))

    @property
    def cmds(self) -> List[str]:
        return self._cmds

    @property
    def exec_cmd(self) -> str:
        return self._exec_cmd

    @property
    def tags(self) -> TagCollection:
        return self._tags

    @tags.setter
    def tags(self, value: TagCollection) -> None:
        if value.common_class is SlurmTag:
            self._tags = value
        else:
            err = "`value.common_class` must be SlurmTag"
            raise ValueError(err)
