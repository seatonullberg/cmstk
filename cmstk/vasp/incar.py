from cmstk.utils import BaseTagCollection
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

    def __init__(self,
                 filepath: Optional[str] = None,
                 tags: Optional[Sequence[Any]] = None) -> None:
        if filepath is None:
            filepath = "INCAR"
        self.filepath = filepath
        self._tags = BaseTagCollection(VaspTag, tags)

    def read(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
            lines = list(map(lambda x: x.strip(), lines))  # remove newlines
            lines = list(filter(None, lines))  # remove empty strings
        tags = self.tags.load_all_tags(base_class=VaspTag,
                                       module_str="cmstk.vasp.incar_tags")
        for line in lines:
            is_valid = False
            for tag in tags:
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
            for _, tag in self.tags:
                f.write(tag.write())

    @property
    def tags(self) -> BaseTagCollection:
        return self._tags
