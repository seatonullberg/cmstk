from cmstk.utils import BaseTag, BaseTagSequence, within_one_percent
import pytest


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
        super().__init__(comment, name, valid_options, value)


def test_base_tag():
    """Tests initialization of a BaseTag object."""
    comment = "test"
    name = "TestTag"
    valid_options = ["test", float]
    value = 0.0
    base_tag = BaseTag(comment, name, valid_options, value)
    base_tag.value = "test"
    with pytest.raises(ValueError):
        base_tag.value = 1


def test_base_tag_sequence():
    """Tests initialization of a BaseTagSequence object."""
    test_tag0 = MockBaseTag()
    test_tag0.name = "zero"
    test_tag1 = MockBaseTag()
    test_tag1.name = "one"
    sequence = BaseTagSequence(base_class=MockBaseTag, 
                               tags=[test_tag0, test_tag1])
    assert len(sequence._tags) == 2
    test_tag2 = MockBaseTag()
    test_tag2.name = "two"
    sequence.append(test_tag2)
    assert len(sequence._tags) == 3
    with pytest.raises(ValueError):
        sequence.append(test_tag0)
    test_tag4 = "not a tag"
    with pytest.raises(ValueError):
        sequence.append(test_tag4)
    assert len(sequence._tags) == 3
    for tag in sequence:
        assert type(tag) is MockBaseTag
    tag = sequence["one"]
    assert tag.name == "one"
    del sequence["one"]
    assert len(sequence._tags) == 2
