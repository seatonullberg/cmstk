import os
from typing import Any, Dict, List, Optional, Sequence


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
        if len(value_section.split()) > 1:
            comment = value_section.split("#")[1].strip()
        else:
            comment = "no comment specified"
        value = value_section.split("#")[0].strip()
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
        return "{} {} = {} # {}".format(self.prefix, self.name, self.value, self.comment).strip()
