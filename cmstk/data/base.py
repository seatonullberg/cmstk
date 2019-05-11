import os
import json
import type_sanity as ts
from xml.etree import ElementTree
from cmstk.exceptions import ReadOnlyError


class BaseDataReader(object):
    """Representation of an access point to the top level data directory.
    Provides read-only protections to the underlying data.
    
    Args:
        path (optional) (str): A replacement path if the default data directory is not desired.
    """

    def __init__(self, path=None):
        ts.is_type_any((path, [str, type(None)], "path"))
        self._path = path
        self._data = None

    ################
    #  Properties  #
    ################

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

    ##################
    #  Read Methods  #
    ##################

    def read_json(self, filename):
        """
        Reads a JSON file into a dict.
        Sets self._data.

        Args:
            filename (str): Name of a JSON file in the data directory.
        """
        ts.is_type((filename, str, "filename"))
        json_path = os.path.join(self.path, filename)
        with open(json_path) as f:
            json_data = json.load(f)

        self._data = json_data

    def read_text(self, filename):
        """Reads a generic text file into a list of \n separated lines.
        
        Args:
            filename (str): Name of the text file in the data directory.
        """
        ts.is_type((filename, str, "filename"))
        text_path = os.path.join(self.path, filename)
        with open(text_path) as f:
            text_data = f.readlines()

        self._data = text_data

    def read_xml(self, filename):
        """Reads an xml file into an ElementTree object.
        
        Args:
            filename (str): Name of the xml file in the data directory.
        """
        ts.is_type((filename, str, "filename"))
        xml_path = os.path.join(self.path, filename)
        xml_data = ElementTree.parse(xml_path).getroot()

        self._data = xml_data

    #######################
    #  Method Overriding  #
    #######################

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
