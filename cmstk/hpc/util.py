from cmstk.filetypes import TextFile
from cmstk.util import BaseFileNotifier, BaseTag
from typing import List, Optional


class SubmissionScript(TextFile):
    """Generalized representation of a job submission script for high
       performance computing job managers.

    Args:
        filepath: Filepath to a script.
        exec_cmd: The shell command used to execute the script.
        cmds: Commands to be executed.
        tags: Tags used to configure the job manager.

    Attributes:
        filepath: Filepath to a script.
        cmds: Commands to be executed.
        exec_cmd: The shell command used to execute the script.
        tags: Tags used to configure the job manager.
    """

    def __init__(self, filepath: str, exec_cmd: str,
                 cmds: Optional[List[str]], tags: Optional[List[BaseTag]]) -> None:
        self.exec_cmd = exec_cmd
        self._cmds = cmds
        self._tags = tags
        super().__init__(filepath)

    @property
    def cmds(self) -> List[str]:
        if self._cmds is None:
            self._cmds = [
                line for line in self.lines[1:]  # skip the shebang
                if not line.startswith(self.prefix)
            ]
        return self._cmds

    @cmds.setter
    def cmds(self, value: List[str]) -> None:
        self._cmds = value

    @property
    def tags(self) -> List[BaseTag]:
        if self._tags is None:
            self._tags = []
            for line in self.lines:
                if line.startswith(self.prefix):
                    self._tags.append(Tag.from_str(line))
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

class BaseJob(object):
    """Representation of an HPC job.

    Args:
        notifiers: Notifier objects to monitor for success or failure.
        submission_script: The job submission script.
    """

    def __init__(self,
                 notifiers: List[BaseFileNotifier],
                 submission_script: SubmissionScript) -> None:
        self.notifiers = notifiers
        self.submission_script = submission_script
