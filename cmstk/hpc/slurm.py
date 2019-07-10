from cmstk.hpc.slurm_tags import SlurmTag
from cmstk.utils import BaseTagSequence
import datetime
import os
from typing import Any, Optional, Sequence


class SubmissionScript(object):
    """File wrapper for a SLURM submission script.
    
    Args:
        filepath: Filepath to a SLURM script.
        tags: The slurm tags to be included in the submission script.

    Attributes:
        filepath: Filepath to an INCAR file.

    Properties:
        tags: Sequence of slurm tag objects which can be accessed like a dict.
    """

    def __init__(self, filepath: Optional[str] = None,
                 tags: Optional[Sequence[Any]] = None) -> None:
        if filepath is None:
            filepath = "runjob.slurm"
        self.filepath = filepath
        self._tags = BaseTagSequence(SlurmTag, tags)

    def read(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
            lines = list(map(lambda x: x.strip(), lines))  # remove newlines
            lines = list(filter(None, lines))  # remove empty strings
        tags = self._load_all_tags()
        for line in lines:
            if not line.startswith("#SBATCH"):
                continue
            is_valid = False
            for _, tag in tags.items():
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
    
    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("#!/bin/bash")
            for tag in self.tags:
                f.write(tag.write())
            # TODO add module loads and such

    @property
    def tags(self) -> BaseTagSequence:
        return self._tags

    @staticmethod
    def _load_all_tags():
        module_str = "cmstk.hpc.slurm_tags"
        module = importlib.import_module(module_str)
        attrs = {name: obj for name, obj in module.__dict__.items()}
        classes = {name: obj for name, obj in attrs.items() 
                   if inspect.isclass(obj)}
        tags = {name: obj for name, obj in classes.items() 
                if issubclass(obj, VaspTag)}
        del tags["SlurmTag"]  # ignore the base class
        tags = {k: v() for k, v in tags.items()}  # initialize the tags
        return tags
