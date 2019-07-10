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
        #self._tags = BaseTagSequence(SlurmTag, tags)