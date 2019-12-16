import json
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


class BaseFile(object):
    """Abstract base class for file wrappers.
    
    Args:
        filepath: The path to the underlying file.
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._attrs = [k for k in self.__dict__ if k[0] == "_"]

    def load(self, path: Optional[str] = None) -> None:
        """Load the underlying file into memory.
        
        Note:
            This must be overridden by the child.
        """
        raise NotImplementedError()

    def unload(self) -> None:
        """Unload the underlying file from memory."""
        for attrs in self._attrs:
            setattr(self, attr, None)

    def __enter__(self):
        self.load()

    def __exit__(self):
        self.unload()


class JsonFile(BaseFile):
    """Generalized representation of a JSON file.
    
    Args:
        filepath: The path to the underlying file.

    Attributes:
        filepath: The path to the underlying file.
        json_data: The json data decoded as a dict.
    """

    def __init__(self, filepath: str) -> None:
        self._json_data = Optional[Dict[str, Any]]
        super().__init__(filepath)

    def load(self, path: Optional[str]) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            self._json_data = json.load(f)

    @property
    def json_data(self) -> Optional[Dict[str, Any]]:
        return self._json_data


class TextFile(BaseFile):
    """Generalized representation of a basic text file.
    
    Args:
        filepath: The path to the underlying file.

    Attributes:
        filepath: The path to the underlying file.
        lines: The lines of the text file.
    """

    def __init__(self, filepath: str) -> None:
        self._lines: Optional[List[str]] = None
        super().__init__(fielpath)

    def load(self, path: Optional[str]) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            self._lines = f.readlines()

    @property
    def lines(self) -> Optional[List[str]]:
        return self._lines


class XmlFile(BaseFile):
    """Generalized representation of an XML file.
    
    Args:
        filepath: The path to the underlying file.

    Attributes:
        filepath: The path to the underlying file.
        root: The root element of the XML tree.
    """

    def __init__(self, filepath: str) -> None:
        self._root: Optional[Element]
        super().__init__(filepath)

    def load(self, path: Optional[str]) -> None:
        if path is None:
            path = self.filepath
        self._root = ET.parse(path).getroot()

    @property
    def root(self) -> Optional[Element]:
        return self._root
