from cmstk.utils import BaseTagCollection
from cmstk.vasp.incar_tags import IncarTag
import os
from typing import Any, Optional, Sequence


class IncarFile(object):
    """File wrapper for a VASP INCAR file.
    
    Args:
        filepath: Filepath to an INCAR file
        tags: The vasp tags to be included in the incar file.

    Attributes:
        filepath: Filepath to an INCAR file.
        tags: Sequence of vasp tag objects which can be accessed like a dict.
    """
    def __init__(self,
                 filepath: Optional[str] = None,
                 tags: Optional[Sequence[Any]] = None) -> None:
        if filepath is None:
            filepath = "INCAR"
        self.filepath = filepath
        self._tags = BaseTagCollection(IncarTag, tags)

    @classmethod
    def from_default(cls, 
                     name: str, 
                     filepath: Optional[str] = None,
                     json_path: Optional[str] = None):
        """Initializes from predefined settings.

        Notes:
            The predefined settings are assumed to be in a json file located at
            the environment variable CMSTK_INCAR_DEFAULTS or passed absolutely 
            in the parameter `json_path`. The `json_path` parameter takes
            precedence.
        
        Args:
            name: The name of the default setting to use.
            filepath: Filepath to an INCAR file.
            json_path: Filepath to the json defaults file.
        
        Raises:
            ValueError:
            - Unable to load defaults without value for CMSTK_INCAR_DEFAULTS.
        """
        if json_path is None:
            json_path = os.getenv("CMSTK_INCAR_DEFAULTS")
        if json_path is None:
            err = (
                "Unable to load defaults without value for "
                "CMSTK_INCAR_DEFAULTS."
            )
            raise ValueError(err)
        base_class = IncarTag
        module_str = "cmstk.vasp.incar_tags"
        tags = BaseTagCollection.from_default(
            base_class=base_class,
            module_str=module_str,
            name=name,
            path=json_path
        )
        incar = cls(filepath=filepath)
        incar._tags = tags  # this is sort of gross
        return incar

    def read(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
            lines = list(map(lambda x: x.strip(), lines))  # remove newlines
            lines = list(filter(None, lines))  # remove empty strings
        tags = self.tags.load_all_tags(base_class=IncarTag,
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
