from cmstk.utils import BaseTagSequence
from cmstk.vasp.incar_tags import VaspTag
from typing import Any, Optional, Sequence


class IncarFile(object):
    """File wrapper for a VASP INCAR file.
    
    Args:
        filepath: Filepath to an INCAR file
        tags: The vasp tags to be included in the incar file.

    Attributes:
        filepath: Filepath to an INCAR file.

    Properties:
        tags: Sequence of vasp tag objects which can be accessed like a dict.
    """

    def __init__(self, filepath: Optional[str] = None,
                 tags: Optional[Sequence[Any]] = None) -> None:
        if filepath is None:
            filepath = "INCAR"
        self.filepath = filepath
        self._tags = BaseTagSequence(VaspTag, tags)

    def read(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        pass


    def write(self, path: Optional[str] = None) -> None: 
        if path is None:
            path = self.filepath
        pass

    @property
    def tags(self) -> BaseTagSequence:
        return self._tags

    @staticmethod
    def _load_all_tags():
        module_str = "cmstk.vasp.incar_tags"
        module = importlib.import_module(module_str)
        attrs = {name: obj for name, obj in module.__dict__.items()}
        classes = {name: obj for name, obj in attrs.items() 
                   if inspect.isclass(obj)}
        tags = {name: obj for name, obj in classes.items() 
                if issubclass(obj, VaspTag)}
        del tags["VaspTag"]  # ignore the base class
        return tags
