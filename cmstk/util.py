import importlib
import inspect
import os
from typing import Any, Dict, List, Optional, Sequence

#========================#
#    Helper Functions    #
#========================#


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

    Attributes:
        value: The value of the tag.
    """

    def __init__(self,
                 name: str,
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


class TagCollection(object):
    """Collection of tags which closely mimics the interface of a dict.
    
    Args:
        common_class: The class which all members must be an instance of.
        tags: The tag objects to store.
    """

    def __init__(self, common_class: type,
                 tags: Optional[List[Any]] = None) -> None:
        if not issubclass(common_class, BaseTag):
            err = "`common_class` must be a subclass of BaseTag"
            raise TypeError(err)
        self._common_class = common_class
        self._tags: Dict[str, BaseTag] = {}
        if tags is not None:
            for tag in tags:
                self.insert(tag)

    @classmethod
    def from_default(cls, common_class: type, json_data: Dict[str, Any],
                     module: str):
        """Initializes from a predefined json file.

        Args:
            common_class: The class which all members must be an instance of.
            json_input: Dict of raw json data.
            module: Name of the module to import tags from.
        """
        valid_tags = {
            tag.name: tag for tag in cls.import_tags(common_class, module)
        }
        tags = []
        for k, v in json_data.items():
            if k not in valid_tags:
                err = "`{}` is not a valid key for any tag in `{}`".format(
                    k, module)
                raise KeyError(err)
            tag = valid_tags[k]
            tag.value = v
            tags.append(tag)
        return cls(common_class=common_class, tags=tags)

    @staticmethod
    def import_tags(common_class: type, module: str) -> List[Any]:
        """Imports tag objects from a module.
        
        Args:
            common_class: The class which all members must be an instance of.
            module: Name of the module to import from.
        """
        attributes = importlib.import_module(module).__dict__
        classes = {
            name: obj
            for name, obj in attributes.items()
            if inspect.isclass(obj)
        }
        tags = {
            name: obj
            for name, obj in classes.items()
            if issubclass(obj, common_class)
        }
        del tags[common_class.__name__]  # do not import the base class
        return [v() for v in tags.values()]

    def __setitem__(self, key, value):
        if key in self._tags:
            # set the `value` attribute of the item rather than the item itself
            self._tags[key].value = value
        else:
            err = "key `{}` not found in self._tags".format(key)
            raise KeyError(err)

    def insert(self, value: BaseTag) -> None:
        """Inserts a tag object into the collection.
        
        Args:
            value: The tag to be inserted.

        Raises:
            TypeError:
            - `value` must be an instance of {common_class}.
        """
        if not isinstance(value, self._common_class):
            err = "`value` must be an instance of {}".format(self._common_class)
            raise TypeError(err)
        self._tags[value.name] = value

    @property
    def common_class(self) -> type:
        return self._common_class

    # dict interface wrappers

    def get(self, key, default=None):
        return self._tags.get(key, default)

    def items(self):
        return self._tags.items()

    def keys(self):
        return self._tags.keys()

    def values(self):
        return self._tags.values()

    def __contains__(self, key):
        return self._tags.__contains__(key)

    def __getitem__(self, key):
        return self._tags.__getitem__(key)

    def __delitem__(self, key):
        return self._tags.__delitem__(key)

    def __iter__(self):
        return self._tags.__iter__()

    def __len__(self):
        return self._tags.__len__()
