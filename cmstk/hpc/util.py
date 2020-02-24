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
        shebang: The shell specific shebang symbol.

    Attributes:
        filepath: Filepath to a script.
        cmds: Commands to be executed.
        exec_cmd: The shell command used to execute the script.
        tags: Tags used to configure the job manager.
        shebang: The shell specific shebang symbol.
    """

    def __init__(self,
                 filepath: str,
                 cmds: Optional[List[str]] = None,
                 tags: Optional[List[BaseTag]] = None,
                 shebang: Optional[str] = None) -> None:
        self._cmds = cmds
        self._tags = tags
        self._shebang = shebang
        super().__init__(filepath)

    @property
    def cmds(self) -> List[str]:
        raise NotImplementedError

    @cmds.setter
    def cmds(self, value: List[str]) -> None:
        self._cmds = value

    @property
    def exec_cmd(self) -> str:
        raise NotImplementedError

    @property
    def tags(self) -> List[BaseTag]:
        raise NotImplementedError

    @tags.setter
    def tags(self, value: List[BaseTag]) -> None:
        self._tags = value

    @property
    def shebang(self) -> str:
        if self._shebang is None:
            self._shebang = self.lines[0].strip()
        return self._shebang

    @shebang.setter
    def shebang(self, value: str) -> None:
        self._shebang = value

    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("{}\n".format(self.shebang))
            for tag in self.tags:
                f.write("{}\n".format(str(tag)))
            f.write("\n")
            for cmd in self.cmds:
                f.write("{}\n".format(cmd))
