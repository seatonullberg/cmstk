from cmstk.filetypes import TextFile
from cmstk.util import BaseTag
from typing import List, Optional


class BaseSubmissionScript(TextFile):
    """Generalized representation of a job submission script for high
       performance computing job managers.

    Args:
        filepath: Filepath to a script.
        cmds: Commands to be executed.
        tags: Tags used to configure the job manager.

    Attributes:
        filepath: Filepath to a script.
        cmds: Commands to be executed.
        exec_cmd: The shell command used to execute the script.
        tags: Tags used to configure the job manager.
    """

    _exec_cmd = ""
    _tag_type = BaseTag

    def __init__(self,
                 filepath: str,
                 cmds: Optional[List[str]] = None,
                 tags: Optional[List[BaseTag]] = None) -> None:
        self._cmds = cmds
        self._tags = tags
        super().__init__(filepath)

    @property
    def cmds(self) -> List[str]:
        if self._cmds is None:
            self._cmds = [
                line for line in self.lines[1:]  # skip the shebang
                if not line.startswith(self._tag_type._name_prefix)
            ]
        return self._cmds

    @cmds.setter
    def cmds(self, value: List[str]) -> None:
        self._cmds = value

    @property
    def exec_cmd(self) -> str:
        return self._exec_cmd

    @property
    def tags(self) -> List[BaseTag]:
        if self._tags is None:
            self._tags = [
                self._tag_type.from_str(line)
                for line in self.lines
                if line.startswith(self._tag_type._name_prefix)
            ]
        return self._tags

    @tags.setter
    def tags(self, value: List[BaseTag]) -> None:
        self._tags = value

    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("#!/bin/bash\n")
            for tag in self.tags:
                f.write("{}\n".format(tag.to_str()))
            f.write("\n")
            for cmd in self.cmds:
                f.write("{}\n".format(cmd))
