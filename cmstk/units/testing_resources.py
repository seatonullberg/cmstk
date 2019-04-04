def within_one_percent(target, actual):
    # returns True if actual is within 1 percent of target
    upper = target + (target*0.01)
    lower = target - (target*0.01)
    return lower < actual < upper