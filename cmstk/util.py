import os
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


class BaseTag(object):
    """Generic representation of a tag/flag/variable for a generic input script.

    Args:
        comment: Description of the tag's purpose.
        name: The tag's name.
        value: The value of the tag.

    Attributes:
        comment: Description of the tag's purpose.
        name: The tag's name.
        value: The value of the tag.
    """

    def __init__(self,
                 name: Optional[str] = None,
                 comment: Optional[str] = None,
                 value: Any = None) -> None:
        if name is None:
            name = ""
        self.name: str = name
        if comment is None:
            comment = "no comment specified"
        self.comment: str = comment
        self.value = value

    @classmethod
    def from_str(cls, s: str) -> 'BaseTag':
        """Initializes a BaseTag object by parsing info directly from a string."""
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
