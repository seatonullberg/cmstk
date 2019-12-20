import datetime
import os
import time
from typing import Any, List, Optional, Sequence


def consecutive_percent_difference(x: Sequence) -> List:
    """Returns a list of the percent difference between each consecutive member
       of the sequence `x`.
    """
    return [((_x - x[i - 1]) / x[i - 1]) * 100 if i > 0 else 0
            for i, _x in enumerate(x)]


def data_directory() -> str:
    """Returns the absolute path to the data directory."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    return os.path.join(path, "data")


def within_one_percent(a: float, b: float) -> bool:
    """Returns True if a is within 1% of b."""
    diff = abs(a - b)
    return abs(diff / b) < 0.01


class FileNotifier(object):
    """Notifier which monitors a file for changes.
    
    Args:
        filepath: Path to a file to monitor.
        delay: The time to wait between polls.
        failure_triggers: List of strings which indicate failure.
        success_triggers: List of strings which indicate success.
        time_limit: The maximum amount of time to wait before raising an 
            exception.
    """

    def __init__(self,
                 filepath: str,
                 delay: Optional[datetime.timedelta] = None,
                 failure_triggers: Optional[List[str]] = None,
                 success_triggers: Optional[List[str]] = None,
                 time_limit: Optional[datetime.timedelta] = None) -> None:
        self.filepath = filepath
        if delay is None:
            delay = datetime.timedelta(minutes=15)
        self.delay = delay
        if failure_triggers is None:
            failure_triggers = []
        self.failure_triggers = []
        if success_triggers is None:
            success_triggers = []
        self.success_triggers = success_triggers
        self.time_limit = time_limit

    def run(self) -> None:
        """Monitors a file until it contains a failure trigger, success trigger,
        or reaches the maximum time limit."""
        start = datetime.datetime.now() 
        while True:
            time.sleep(self.delay.total_seconds())
            with open(self.filepath, "r") as f:
                content = f.read()
            for ft in self.failure_triggers:
                if ft in content:
                    raise RuntimeError()
            for st in self.success_triggers:
                if st in content:
                    return
            if self.time_limit is not None:
                elapsed_time = datetime.datetime.now() - start
                if elapsed_time > self.time_limit:
                    raise RuntimeError()


class Tag(object):
    """Representation of a tag/flag/variable for a generic input script.

    Args:
        name: The tag's name.
        comment: Description of the tag's purpose.
        prefix: Marker indicating a line should be treated as a tag.
        value: The value of the tag.

    Attributes:
        name The tag's name
        comment: Description of the tag's purpose.
        prefix: Marker indicating a line should be treated as a tag.
        value: The value of the tag.
    """

    def __init__(self,
                 name: Optional[str] = None,
                 comment: Optional[str] = None,
                 prefix: Optional[str] = None,
                 value: Any = None) -> None:
        if name is None:
            name = ""
        self._name = name
        if comment is None:
            comment = "no comment specified"
        self._comment = comment
        if prefix is None:
            prefix = ""
        self._prefix = prefix
        self._value = value

    @classmethod
    def from_str(cls, s: str) -> 'Tag':
        """Parses tag info from a string into a Tag object.

        Notes:
            The string should have the form:
            <prefix> <name> = <value> # <comment>

        Args:
            s: The string to parse.
        """
        name_section = s.split("=")[0]
        if len(name_section.split()) > 1:
            prefix = name_section.split()[0].strip()
        else:
            prefix = ""
        name = name_section.replace(prefix, "").strip()
        value_section = s.split("=")[1]
        if "#" in value_section:
            value = value_section.split("#")[0].strip()
            comment = value_section.split("#")[1].strip()
        else:
            value = value_section.strip()
            comment = "no comment specified"
        return Tag(name, comment, prefix, value)

    @property
    def name(self) -> str:
        return self._name

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def value(self) -> Any:
        return self._value

    def to_str(self) -> str:
        """Writes the tag info into a string."""
        return "{} {} = {} # {}".format(self.prefix, self.name, self.value,
                                        self.comment).strip()
