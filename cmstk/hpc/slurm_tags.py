from cmstk.utils import BaseTag
import datetime
import re
from typing import Any, Optional, Sequence, Tuple


class SlurmTag(BaseTag):
    """Representation of a generic SLURM tag.
    
    Args:
        name: SLURM compliant tag name.
        valid_options: The values this tag accepts.
        comment: Description of the tag.
        value: Value assigned to the tag.
    """

    def __init__(self, name: str,
                 valid_options: Sequence[Any],
                 comment: Optional[str] = None,
                 value: Optional[Any] = None) -> None:
        super().__init__(name=name, valid_options=valid_options,
                         comment=comment, value=value)

    def _read_int(self, line: str) -> None:
        pass
    
    def _read_str(self, line: str) -> None:
        pass

    def _read_time(self, line: str) -> None:
        pass

    def _read(self, line: str) -> Tuple[str, Optional[str]]:
        pass

    def _write_int(self) -> str:
        pass

    def _write_str(self) -> str:
        pass

    def _write_time(self) -> str:
        pass

    def _wrtie(self, str_value: str) -> str:
        pass

#=================================#
#    SLURM Tag Implementations    #
#=================================#

class AccountTag(BaseTag):
    
    def __init__(self, value=None):
        name = "account"
        comment = "User account name."
        valid_options = [str]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class DistributionTag(BaseTag):
    
    def __init__(self, value=None):
        name = "distribution"
        comment = "Distribution method for remote processes."
        valid_options = [
            "block:block", "block:cyclic", "block:fcyclic",
            "cyclic:block", "cyclic:cyclic", "cyclic:fcyclic",
            "plane:block", "plane:cyclic", "plane:fcyclic",
            "arbitrary:block", "arbitrary:cyclic", "arbitrary:fcyclic"
        ]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class ErrorTag(BaseTag):
    
    def __init__(self, value=None):
        name = "error"
        comment = "Filename to write stderr to."
        valid_options = [str]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class JobNameTag(BaseTag):
    
    def __init__(self, value=None):
        name = "job-name"
        comment = "Name of the job."
        valid_options = [str]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class MailTypeTag(BaseTag):
    
    def __init__(self, value=None):
        name = "mail-type"
        comment = "Email event triggers."
        # any combination of NONE,BEGIN,END,FAIL,REQUEUE,ALL
        valid_options = [str]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class MailUserTag(BaseTag):
    
    def __init__(self, value=None):
        name = "mail-user"
        comment = "Email address to send to."
        valid_options = [str]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class MemPerCpuTag(BaseTag):
    
    def __init__(self, value=None):
        name = "mem-per-cpu"
        comment = "Memory to allocate on each CPU (in MB)."
        valid_options = [int]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class NtasksTag(BaseTag):
    
    def __init__(self, value=None):
        name = "ntasks"
        comment = "Number of tasks to run."
        valid_options = [int]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class OutputTag(BaseTag):
    
    def __init__(self, value=None):
        name = "output"
        comment = "Filename to write stdout to."
        valid_options = [str]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class QosTag(BaseTag):
    
    def __init__(self, value=None):
        name = "qos"
        comment = "QOS account name."
        valid_options = [str]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)


class TimeTag(BaseTag):
    
    def __init__(self, value=None):
        name = "time"
        comment = "Maximum duration of the job."
        valid_options = [datetime.timedelta]
        super().__init__(name=name, comment=comment,
                         valid_options=valid_options, value=value)
