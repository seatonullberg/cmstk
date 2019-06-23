import os
import math


def within_one_percent(a, b):
    """Returns True if a is within 1% of b."""
    diff = math.sqrt((a - b)**2)
    return (diff / b) < 0.01

def  data_directory():
    """Returns the absolute path to the data directory."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "data")
    return path
