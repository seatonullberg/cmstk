from cmstk.utils import BaseTag, BaseTagCollection, within_one_percent, consecutive_percent_difference
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


def test_base_tag_collection():
    """Tests initialization of a BaseTagCollection object."""
    test_tag0 = MockBaseTag()
    test_tag0.name = "zero"
    test_tag1 = MockBaseTag()
    test_tag1.name = "one"
    collection = BaseTagCollection(base_class=MockBaseTag,
                                   tags=[test_tag0, test_tag1])
    assert len(collection._tags) == 2
    test_tag2 = MockBaseTag()
    test_tag2.name = "two"
    collection.append(test_tag2)
    assert len(collection._tags) == 3
    with pytest.raises(ValueError):
        collection.append(test_tag0)
    test_tag4 = "not a tag"
    with pytest.raises(ValueError):
        collection.append(test_tag4)
    assert len(collection._tags) == 3
    for tag_name, tag in collection:
        assert type(tag) is MockBaseTag
    tag = collection["one"]
    assert tag.name == "one"
    del collection["one"]
    assert len(collection._tags) == 2
