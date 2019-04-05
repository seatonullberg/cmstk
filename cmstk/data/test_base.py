from cmstk.data.base import BaseDataReader
from cmstk.data.exceptions import ReadOnlyError
import os
import pytest


def test_init_base_data_reader():
    # tests if BaseDataReader can be initialized
    bdr = BaseDataReader()
    assert bdr._path is None

def test_base_data_reader_path():
    # tests default BaseDataReader path
    bdr = BaseDataReader()
    path = bdr.path
    assert os.path.basename(path) == "data"

def test_base_data_reader_read_json():
    # tests BaseDataReader read_json method
    bdr = BaseDataReader()
    json_data = bdr.read_json("elements.json")
    assert json_data["C"]["atomic_radius"] == 67

def test_base_data_reader_access():
    # tests if BaseDataReader provides read access.
    # tests if BaseDataReader denies write/delete access.
    bdr = BaseDataReader()
    bdr._data = bdr.read_json("elements.json")
    # read access
    assert bdr["C"]["atomic_radius"] == 67
    # write access
    with pytest.raises(ReadOnlyError):
        bdr["C"] = "test_value"
    # delete access
    with pytest.raises(ReadOnlyError):
        del bdr["C"]