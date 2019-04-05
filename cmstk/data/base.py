import os
import json
from cmstk.data.exceptions import ReadOnlyError


class BaseDataReader(object):
    """Representation of an access point to the top level data directory.
    
    Args:
        path (optional) (str): A replacement path if the default data directory is not desired.
        filename (optional) (str): A specific file to read on init.
    """

    def __init__(self, path=None, filename=None):
        self._path = path
        if filename is not None:
            self._data = self.read_json(filename)
        else:
            self._data = None

    @property
    def path(self):
        """
        Returns:
             (str): Absolute path to the top level data directory or a custom data directory.
        """
        # check for a user defined path first
        if self._path is not None:
            return self._path
        # otherwise use the default data directory
        path = os.path.abspath(__file__)  # start at current path (cmstk/cmstk/data/base.py)
        path = os.path.dirname(path)  # go up one level (cmstk/cmstk/data)
        path = os.path.dirname(path)  # go up another level (cmstk/cmstk)
        path = os.path.dirname(path)  # go up one more level (cmstk)
        path = os.path.join(path, "data")  # final result (cmstk/data)
        return path

    def read_json(self, filename):
        """
        Reads JSON files.

        Args:
            filename (str): Name of a JSON file in the data directory.
        Returns:
            (dict): Parsed content from filename.
        """
        if type(filename) is not str:
            raise TypeError("`filename` must be of type str")
        
        json_path = os.path.join(self.path, filename)
        with open(json_path) as f:
            json_data = json.load(f)

        return json_data

    def __getitem__(self, key):
        if self._data is None:
            raise RuntimeError("self._data has not yet been set")
        return self._data[key]

    def __iter__(self):
        if self._data is None:
            raise RuntimeError("self._data has not yet been set")
        return self._data.__iter__()

    def __missing__(self, key):
        if self._data is None:
            raise RuntimeError("self._data has not yet been set")
        return self._data.__missing__(key)

    def __reversed__(self):
        if self._data is None:
            raise RuntimeError("self._data has not yet been set")
        return self._data.__reversed__()

    def __contains__(self, item):
        if self._data is None:
            raise RuntimeError("self._data has not yet been set")
        return self._data.__contains__(item)

    def __setitem__(self, key, value):
        raise ReadOnlyError(name=self.__class__.__name__, operation="__setitem__")

    def __delitem__(self, key):
        raise ReadOnlyError(name=self.__class__.__name__, operation="__delitem__") 

    