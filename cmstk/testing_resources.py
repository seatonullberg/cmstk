import os


def within_one_percent(a, b):
    """Returns True if a is within 1% of b."""
    upper = b * 1.01
    lower = b * 0.99
    return lower < a < upper

def  data_directory():
    """Returns the absolute path to the data directory."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "data")
    return path