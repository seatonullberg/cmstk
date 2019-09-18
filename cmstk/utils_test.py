from cmstk.utils import BaseTag, TagCollection, within_one_percent, consecutive_percent_difference
import pytest


def test_consecutive_percent_difference():
    """Tests behavior of the utility function consecutive_percent_difference."""
    x = [100, 50, 10, 1]
    deltas = consecutive_percent_difference(x)
    assert deltas == [0, -50, -80, -90]


def test_within_one_percent():
    """Tests behavior of the utillity function within_one_percent."""
    a = 1.0
    b = 0.99
    assert not within_one_percent(a, b)
    b = 0.999
    assert within_one_percent(a, b)
    a = -1.0
    b = -0.99
    assert not within_one_percent(a, b)
    b = -0.999
    assert within_one_percent(a, b)


class MockBaseTag(BaseTag):
    def __init__(self):
        comment = "test"
        name = "TestTag"
        valid_options = ["test", float]
        value = 0.0
        super().__init__(name, valid_options, comment, value)


def test_base_tag():
    """Tests initialization of a BaseTag object."""
    comment = "test"
    name = "TestTag"
    valid_options = ["test", float]
    value = 0.0
    base_tag = BaseTag(name, valid_options, comment, value)
    base_tag.value = "test"
    with pytest.raises(ValueError):
        base_tag.value = 1


def test_tag_collection():
    """Tests initialization of a TagCollection object."""
    test_tag0 = MockBaseTag()
    test_tag0.name = "zero"
    test_tag1 = MockBaseTag()
    test_tag1.name = "one"
    # basic initialization
    collection = TagCollection(common_class=MockBaseTag,
                               tags=[test_tag0, test_tag1])
    with pytest.raises(ValueError):
        _ = TagCollection(common_class=object)
    # len
    assert len(collection) == 2
    # setitem/getitem
    collection["zero"] = 0.0
    assert type(collection["zero"]) is MockBaseTag
    assert collection["zero"].value == 0.0
    # contains
    assert "zero" in collection
    # delitem
    del collection["zero"]
    assert "zero" not in collection
    # iter
    assert len([key for key in collection]) == 1
    # insert
    test_tag2 = MockBaseTag()
    test_tag2.name = "two"
    collection.insert(test_tag2)
    assert len(collection) == 2
    test_tag4 = "not a tag"
    with pytest.raises(ValueError):
        collection.insert(test_tag4)
    assert len(collection) == 2
    # items
    for key, value in collection.items():
        assert type(key) is str
        assert type(value) is MockBaseTag
    # keys
    for key in collection.keys():
        assert type(key) is str
    # values
    for value in collection.values():
        assert type(value) is MockBaseTag
