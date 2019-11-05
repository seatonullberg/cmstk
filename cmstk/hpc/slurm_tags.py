from cmstk.util import BaseTag
import datetime
import math
from typing import Any, Optional, Sequence, Tuple


class SlurmTag(BaseTag):
    """Representation of a generic SLURM tag.
    
    Args:
        name: SLURM compliant tag name.
        valid_options: The values this tag accepts.
        comment: Description of the tag.
        value: Value assigned to the tag.
    """

    def __init__(self,
                 name: str,
                 valid_options: Sequence[Any],
                 comment: Optional[str] = None,
                 value: Optional[Any] = None) -> None:
        super().__init__(name=name,
                         valid_options=valid_options,
                         comment=comment,
                         value=value)

    def _read_int(self, line: str) -> None:
        """Reads in tag content with value interpreted as int.
        
        Args:
            line: The string to parse.
        """
        value, self.comment = self._read(line)
        self.value = int(value)

    def _read_str(self, line: str) -> None:
        """Reads in tag content with value interpreted as str.
        
        Args:
            line: The string to parse.
        """
        self.value, self.comment = self._read(line)

    def _read_time(self, line: str) -> None:
        """Reads in tag content with value interpreted as a duration.
        
        Args:
            line: The string to parse.
        """
        value, self.comment = self._read(line)
        hours, mins, secs = value.split(":")
        self.value = datetime.timedelta(hours=int(hours),
                                        minutes=int(mins),
                                        seconds=int(secs))

    def _read(self, line: str) -> Tuple[str, Optional[str]]:
        """Reads raw tag content (value, comment) from a line of text.
        
        Args:
            line: The string to parse.

        Raises:
            ValueError:
            - if the parsed name does not match the tag's name
            - If no value is found
        """
        name = " ".join(line.split()[1:])  # TODO: this is not really the name
        name, value = name.split("=")
        if name != self.name:
            err = ("tag with name `{}` cannot be parsed by {}".format(
                name, self.__class__))
            raise ValueError(err)
        comment: Optional[str]
        if "#" in value:
            value, comment = value.split("#")
            comment = comment.strip()
        else:
            comment = None
        value = value.strip()
        if value == "":
            err = "unable to find value in line: {}".format(line)
            raise ValueError(err)
        return (value, comment)

    def _write_int(self) -> str:
        """Writes a line of tag info with the value interpreted as int."""
        str_value = str(self.value)
        return self._write(str_value)

    def _write_str(self) -> str:
        """Writes a line of tag info with the value interpreted as str."""
        return self._write(self.value)

    def _write_time(self) -> str:
        """Writes a line of tag info with the value interpreted as duration."""
        total_seconds = self.value.total_seconds()
        hours = total_seconds / (60 * 60)
        minutes = (hours - math.floor(hours)) * 60
        seconds = (minutes - math.floor(minutes)) * 60
        s = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes),
                                          int(seconds))
        return self._write(s)

    def _write(self, str_value: str) -> str:
        """Writes a single line string from preprocessed tag info.

        Args:
            str_value: The tag's value formatted as SLURM compliant text.

        Raises:
            ValueError
            - If `str_value` is ""
        """
        if str_value == "":
            err = "writing a None value may have unforseen consequences"
            raise ValueError(err)
        if self.comment is None:
            s = "#SBATCH {}={}\n".format(self.name, str_value)
        else:
            s = "#SBATCH {}={}\t# {}\n".format(self.name, str_value,
                                               self.comment)
        return s


#=================================#
#    SLURM Tag Implementations    #
#=================================#


class AccountTag(SlurmTag):

    def __init__(self, value=None):
        name = "--account"
        comment = "User account name."
        valid_options = [str]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class DistributionTag(SlurmTag):

    def __init__(self, value=None):
        name = "--distribution"
        comment = "Distribution method for remote processes."
        valid_options = [
            "block:block", "block:cyclic", "block:fcyclic", "cyclic:block",
            "cyclic:cyclic", "cyclic:fcyclic", "plane:block", "plane:cyclic",
            "plane:fcyclic", "arbitrary:block", "arbitrary:cyclic",
            "arbitrary:fcyclic"
        ]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class ErrorTag(SlurmTag):

    def __init__(self, value=None):
        name = "--error"
        comment = "Filename to write stderr to."
        valid_options = [str]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class JobNameTag(SlurmTag):

    def __init__(self, value=None):
        name = "--job-name"
        comment = "Name of the job."
        valid_options = [str]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class MailTypeTag(SlurmTag):

    def __init__(self, value=None):
        name = "--mail-type"
        comment = "Email event triggers."
        # any combination of NONE,BEGIN,END,FAIL,REQUEUE,ALL
        valid_options = [str]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class MailUserTag(SlurmTag):

    def __init__(self, value=None):
        name = "--mail-user"
        comment = "Email address to send to."
        valid_options = [str]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class MemPerCpuTag(SlurmTag):

    def __init__(self, value=None):
        name = "--mem-per-cpu"
        comment = "Memory to allocate on each CPU (in MB)."
        valid_options = [int]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class NtasksTag(SlurmTag):

    def __init__(self, value=None):
        name = "--ntasks"
        comment = "Number of tasks to run."
        valid_options = [int]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_int(line)

    def write(self):
        return self._write_int()


class OutputTag(SlurmTag):

    def __init__(self, value=None):
        name = "--output"
        comment = "Filename to write stdout to."
        valid_options = [str]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class QosTag(SlurmTag):

    def __init__(self, value=None):
        name = "--qos"
        comment = "QOS account name."
        valid_options = [str]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_str(line)

    def write(self):
        return self._write_str()


class TimeTag(SlurmTag):

    def __init__(self, value=None):
        name = "--time"
        comment = "Maximum duration of the job."
        valid_options = [datetime.timedelta]
        super().__init__(name=name,
                         comment=comment,
                         valid_options=valid_options,
                         value=value)

    def read(self, line: str):
        return self._read_time(line)

    def write(self):
        return self._write_time()
