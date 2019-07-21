import importlib
import inspect
import os
from typing import Any, Dict, List, Optional, Sequence, Union


#====================#
#    Type Aliases    #
#====================#


Number = Union[float, int]


#========================#
#    Helper Functions    #    
#========================#


def  data_directory() -> str:
    """Returns the absolute path to the data directory."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    return os.path.join(path, "data")


def within_one_percent(a: Number, b: Number) -> bool:
    """Returns True if a is within 1% of b."""
    diff = abs(a - b)
    return abs(diff / b) < 0.01


#==============================#
#    Input Script Utilities    #
#==============================#


class BaseTag(object):
    """Generalized representation of a tag/flag/variable for an input script.
    
    Args:
        name: Official tag name.
        valid_options: Values which can be assigned to this tag.
        comment: Description of the tag's purpose.
        value: The value of the tag.

    Properties:
        value: The value of the tag.
    """

    def __init__(self, name: str, 
                 valid_options: Sequence[Any], 
                 comment: Optional[str] = None,
                 value: Optional[Any] = None) -> None:
        self.comment = comment
        self.name = name
        self.valid_options = valid_options
        self._value = None
        self.value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, v) -> None:
        if v is None:
            self._value = v
            return
        valid = False
        for option in self.valid_options:
            if type(option) is type and type(v) is option:
                valid = True
                break
            if v == option:
                valid = True
                break
        if valid:
            self._value = v
        else:
            err = "`{}` is not a valid value for this tag.".format(v)
            raise ValueError(err)


class BaseTagCollection(object):
    """Generalized safe-access collection of instances of BaseTag.
    
    Args:
        base_class: The class which all members must be an instance of.
        tags: The tag instances to store.
    """

    def __init__(self, base_class: Optional[Any] = None,
                 tags: Optional[Sequence[Any]] = None) -> None:
        if base_class is None:
            base_class = BaseTag
        if not issubclass(base_class, BaseTag):
            err = "`base_class` must be a subclass of BaseTag"
            raise ValueError(err)
        self._base_class = base_class
        if tags is None:
            tags = []
        self._tags: Dict[str, Any] = {}
        for tag in tags:
            self.append(tag)
            
    def append(self, tag: Any) -> None:
        """Appends a tag to the sequence if it is valid.
        
        Args:
            tag: The tag to add
        
        Returns:
            None

        Raises:
            ValueError
            - If the tag is invalid
        """
        if not isinstance(tag, self._base_class):
            err = "`{}` is not a valid tag".format(tag)
            raise ValueError(err)
        elif tag.name in self._tags:
            err = "`{}` is already in the sequence".format(tag.name)
            raise ValueError(err)
        else:
            self._tags[tag.name] = tag

    @staticmethod
    def load_all_tags(base_class: Any, module_str: str) -> List[Any]:
        """Loads all tags from the specified module.
        
        Args:
            base_class: The base tag class.
            module_str: Module to import from.

        Returns:
            List of instances of provided base class
        """
        module = importlib.import_module(module_str)
        attrs = module.__dict__
        classes = {name: obj for name, obj in attrs.items()
                   if inspect.isclass(obj)}
        tags = {name: obj for name, obj in classes.items()
                if issubclass(obj, base_class)}
        del tags[base_class.__name__]
        return [v() for _, v in tags.items()]

    def __iter__(self):
        for k, v in self._tags.items():
            yield k, v

    def __getitem__(self, key):
        return self._tags[key]

    def __delitem__(self, key):
        del self._tags[key]
