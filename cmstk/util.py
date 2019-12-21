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


class BaseFileNotifier(object):
    """Generic notifier which monitors a file for changes.
    
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


class BaseTag(object):
    """Generic representation of a tag/flag/variable for a generic input script.

    Args:
        comment: Description of the tag's purpose.
        name: The tag's name.
        value: The value of the tag.

    Attributes:
        comment: Description of the tag's purpose.
        comment_prefix: Marker indicating a comment will follow.
        name: The tag's name.
        name_prefix: Marker indicating a name will follow.
        value: The value of the tag.
    """

    _comment_prefix: str = "#"
    _name_prefix: str = ""

    def __init__(self,
                 comment: Optional[str] = None,
                 name: Optional[str] = None,
                 value: Any = None) -> None:
        if name is None:
            name = ""
        self._name = name
        if comment is None:
            comment = "no comment specified"
        self._comment = comment
        self._value = value

    @classmethod
    def from_str(cls, s: str) -> 'BaseTag':
        """Parses tag info from a string into a Tag object.

        Notes:
            The string should have the form:
            <name_prefix> <name> = <value> <comment_prefix> <comment>

        Args:
            s: The string to parse.
        """
        name_section = s.split("=")[0]
        name = name_section.replace(cls._name_prefix, "").strip()
        value_section = s.split("=")[1]

        if cls._comment_prefix in value_section:
            value = value_section.split(cls._comment_prefix)[0].strip()
            comment = value_section.split(cls._comment_prefix)[1].strip()
        else:
            value = value_section.strip()
            comment = "no comment specified"
        return cls(comment, name, value)

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._comment = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, v: Any) -> None:
        self._value = v

    def to_str(self) -> str:
        """Writes the tag info into a string."""
        return "{} {} = {} {} {}".format(self._name_prefix, self._name, 
                                         self._value, self._comment_prefix, 
                                         self._comment).strip()
