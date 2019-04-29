import type_sanity as ts
import numpy as np


# TODO: maybe make a ParameterSet object ???


class BaseQOI(object):
    """Representation of a generalized statistical quantity of interest.
    
    Args:
        obj (instance of type BaseQOI): QOI BaseQOI instance used to check for an `evaluate` method.
        name (str): Unique and descriptive identifier.
        target (float): Target value to optimize towards.
        parameters (numpy.ndarray): Parameter set used for evaluation.
    """

    def __init__(self, obj, name, target, parameters):
        ts.is_instance((obj, BaseQOI, "obj"))
        ts.implements((obj, "evaluate", "obj"))
        ts.is_type((name, str, "name"), 
                   (target, float, "target"),
                   (parameters, np.ndarray, "parameters"))
        self._name = name
        self._target = target
        self._parameters = parameters
