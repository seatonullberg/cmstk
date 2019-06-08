from cmstk.units.testing_resources import within_one_percent


def test_within_one_percent():
    target = 100
    actual = 99.5
    assert within_one_percent(target, actual)
    actual = 98.5
    assert not within_one_percent(target, actual)