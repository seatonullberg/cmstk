from cmstk.filetypes import BaseFile, JsonFile, TextFile, XmlFile
import os
import pytest


def test_base_file():
    filepath = "test"
    bf = BaseFile(filepath)
    assert bf.filepath == filepath
    with pytest.raises(NotImplementedError):
        bf.load()


def test_json_file():
    filepath = "test.json"
    content = '{"test_key": "test_value"}'
    with open(filepath, "w") as f:
        f.write(content)
    jf = JsonFile(filepath)
    with pytest.raises(RuntimeError):
        _ = jf.json_data
    jf.load()
    assert jf.json_data["test_key"] == "test_value"
    jf.unload()
    with pytest.raises(RuntimeError):
        _ = jf.json_data
    new_jf = JsonFile(filepath)
    with new_jf:
        assert new_jf.json_data["test_key"] == "test_value"
    with pytest.raises(RuntimeError):
        _ = new_jf.json_data
    os.remove(filepath)


def test_text_file():
    filepath = "test.txt"
    content = "test"
    with open(filepath, "w") as f:
        f.write(content)
    tf = TextFile(filepath)
    with pytest.raises(RuntimeError):
        _ = tf.lines
    tf.load()
    assert tf.lines[0] == content
    tf.unload()
    with pytest.raises(RuntimeError):
        _ = tf.lines
    new_tf = TextFile(filepath)
    with new_tf:
        assert new_tf.lines[0] == content
    with pytest.raises(RuntimeError):
        _ = new_tf.lines
    os.remove(filepath)


def test_xml_file():
    filepath = "test.xml"
    content = '<test>test</test>'
    with open(filepath, "w") as f:
        f.write(content)
    xf = XmlFile(filepath)
    with pytest.raises(RuntimeError):
        _ = xf.root
    xf.load()
    assert xf.root.tag == "test"
    xf.unload()
    with pytest.raises(RuntimeError):
        _ = xf.root
    new_xf = XmlFile(filepath)
    with new_xf:
        assert new_xf.root.tag == "test"
    with pytest.raises(RuntimeError):
        _ = new_xf.root
    os.remove(filepath)
