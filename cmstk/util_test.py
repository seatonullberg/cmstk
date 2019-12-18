from cmstk.util import within_one_percent, consecutive_percent_difference


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
