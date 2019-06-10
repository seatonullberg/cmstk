from cmstk.units.testing_resources import within_one_percent


def test_within_one_percent():
    target = 100
    actual = 99.1
    assert within_one_percent(target, actual)
    actual = 98.9
    assert not within_one_percent(target, actual)