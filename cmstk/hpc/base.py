from cmstk.util import BaseTag, TagCollection
from typing import List, Optional


class BaseScript(object):
    """Generalized representation of a job submission script for high 
       performance computing job managers.

    Args:
        filepath: Filepath to a script.
        cmds: Commands to be executed.
        common_class: The `common_class` parameter for TagCollection.
        exec_cmd: The shell command used to execute the script.
        tags: Tags used to configure the job manager.

    Attributes:
        filepath: Filepath to a script.
        cmds: Commands to be executed.
        exec_cmd: The shell command used to execute the script.
        tags: Tags used to configure the job manager.
    """

    def __init__(self, filepath: str, cmds: List[str], common_class: type,
                 exec_cmd: str, tags: List[BaseTag]) -> None:
        self.filepath = filepath
        self._cmds = cmds
        self._common_class = common_class
        self._tags = TagCollection(self._common_class, tags)
        self._exec_cmd = exec_cmd

    # TODO implement a classmethod to load from_default

    # read does not have a generic implementation

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
        if value.common_class is self._common_class:
            self._tags = value
        else:
            err = "`value.common class` must be {}.".format(self._common_class)
            raise TypeError(err)
