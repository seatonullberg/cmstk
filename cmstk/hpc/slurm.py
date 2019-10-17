from cmstk.hpc.base import BaseScript
from cmstk.hpc.slurm_tags import SlurmTag
from cmstk.utils import BaseTag, TagCollection
import json
import os
from typing import List, Optional


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
                 tags: Optional[List[BaseTag]] = None) -> None:
        if filepath is None:
            filepath = "runjob.slurm"
        if cmds is None:
            cmds = []
        if tags is None:
            tags = []
        super().__init__(filepath=filepath,
                         cmds=cmds,
                         common_class=SlurmTag,
                         exec_cmd="sbatch",
                         tags=tags)

    @classmethod
    def from_default(cls,
                     setting_name: str,
                     filepath: Optional[str] = None,
                     json_path: Optional[str] = None):
        """Initializes from predefined settings.
        
        Notes:
            The predefined settings are assumed to be in a json file located at
            the environment variable CMSTK_HPC_DEFAULTS or passed directly in
            the parameter `json_path`. The `json_path` parameter takes priority.
        
        Args:
            setting_name: The name of the default setting to use.
            filepath: Filepath to a SLURM script.
            json_path: Filepath to the json defaults file.

        Raises:
            ValueError:
            - Unable to load defaults without value for CMSTK_HPC_DEFAULTS.
        """
        if json_path is None:
            json_path = os.getenv("CMSTK_HPC_DEFAULTS")
        if json_path is None:
            err = ("Unable to load defaults without value for "
                   "CMSTK_HPC_DEFAULTS.")
            raise ValueError(err)
        common_class = SlurmTag
        module = "cmstk.hpc.slurm_tags"
        with open(json_path, "r") as f:
            data = json.load(f)[setting_name]
        tag_data = data["tags"]
        cmd_data = data["cmds"]
        tags = TagCollection.from_default(common_class=common_class,
                                          module=module,
                                          json_data=tag_data).values()
        return cls(filepath=filepath, cmds=cmd_data, tags=tags)

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
