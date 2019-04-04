

def within_one_percent(target, actual):
    # returns True if actual is within 1 percent of target
    upper = target + (target*0.01)
    lower = target - (target*0.01)
    return lower < actual < upper

def test_within_one_percent():
    target = 100
    actual = 99.5
    assert within_one_percent(target, actual)
    actual = 98.5
    assert not within_one_percent(target, actual)