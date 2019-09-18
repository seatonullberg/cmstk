from cmstk.utils import BaseTag, TagCollection
from cmstk.vasp.incar_tags import IncarTag
import os
from typing import List, Optional


class IncarFile(object):
    """File wrapper for a VASP INCAR file.
    
    Args:
        filepath: Filepath to an INCAR file
        tags: The vasp tags to be included in the incar file.

    Attributes:
        filepath: Filepath to an INCAR file.
        tags: TagCollection which can be accessed like a dict.
    """
    def __init__(self,
                 filepath: Optional[str] = None,
                 tags: Optional[List[BaseTag]]= None
                ) -> None:
        if filepath is None:
            filepath = "INCAR"
        self.filepath = filepath
        self._tags = TagCollection(IncarTag, tags)

    @classmethod
    def from_default(cls,
                     setting_name: str,
                     filepath: Optional[str] = None,
                     json_path: Optional[str] = None):
        """Initializes from predefined settings.

        Notes:
            The predefined settings are assumed to be in a json file located at
            the environment variable CMSTK_INCAR_DEFAULTS or passed directly in
            the parameter `json_path`. The `json_path` parameter takes priority.
        
        Args:
            setting_name: The name of the default setting to use.
            filepath: Filepath to an INCAR file.
            json_path: Filepath to the json defaults file.
        
        Raises:
            ValueError:
            - Unable to load defaults without value for CMSTK_INCAR_DEFAULTS.
        """
        if json_path is None:
            json_path = os.getenv("CMSTK_INCAR_DEFAULTS")
        if json_path is None:
            err = ("Unable to load defaults without value for "
                   "CMSTK_INCAR_DEFAULTS.")
            raise ValueError(err)
        common_class = IncarTag
        module = "cmstk.vasp.incar_tags"
        tags = TagCollection.from_default(common_class=common_class,
                                          module=module,
                                          setting_name=setting_name,
                                          json_path=json_path).values()
        return cls(filepath=filepath, tags=tags)

    def read(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
            lines = list(map(lambda x: x.strip(), lines))  # remove newlines
            lines = list(filter(None, lines))  # remove empty strings
        tags = self.tags.import_tags(common_class=IncarTag,
                                     module="cmstk.vasp.incar_tags")
        for line in lines:
            is_valid = False
            for tag in tags:
                try:
                    tag.read(line)
                except ValueError:
                    continue
                else:
                    is_valid = True
                    self.tags.insert(tag)
                    break
            if not is_valid:
                err = "unable to parse the following line: {}".format(line)
                raise ValueError(err)

    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            for tag in self.tags.values():
                f.write(tag.write())

    @property
    def tags(self) -> TagCollection:
        return self._tags

    @tags.setter
    def tags(self, value: TagCollection) -> None:
        if value.common_class is IncarTag:
            self._tags = value
        else:
            err = "`value.common_class` must be IncarTag"
            raise ValueError(err)
