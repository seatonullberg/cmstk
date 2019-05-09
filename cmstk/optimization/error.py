import type_sanity as ts
import numpy as np


class BaseErrorFunction(object):
    """Representation of a generalized error function.
    
    Args:
        obj (instance of BaseErrorFunction): Used to check for critical implementation.
    """

    def __init__(self, obj):
        ts.is_instance((obj, BaseErrorFunction, "obj"))
        ts.implements((obj, "calculate_error", "obj"))


class AbsoluteError(BaseErrorFunction):
    """Implementation of absolute error.
    
    Args:
        None
    """

    def __init__(self):
        super().__init__(self)

    def calculate_error(self, target, prediction, normalize=True):
        """Calculates the absolute error between a prediction and its target.
        
        Args:
            target (numpy.ndarray): Array of target values
            prediction (numpy.ndarray): Array of predicted values.
            normalize (optional) (bool): Indicates whether or not to normalize the result.
        """
        ts.is_type((target, np.ndarray, "target"), (prediction, np.ndarray, "prediction"), (normalize, bool, "normalize"))
        err = np.absolute(target - prediction)
        if normalize:
            return err / target
        else:
            return err


class HuberError(BaseErrorFunction):
    """Implementation of Huber error.
    
    Args:
        delta (float): Hyperparameter for tuning the loss.
    """

    def __init__(self, delta):
        ts.is_type((delta, float, "delta"))
        self._delta = delta
        super().__init__(self)

    def calculate_error(self, target, prediction, normalize=True):
        """Calculates the Huber error between a prediction and its target.
        
        Args:
            target (numpy.ndarray): Array of target values
            prediction (numpy.ndarray): Array of predicted values.
            normalize (optional) (bool): Indicates whether or not to normalize the result.
        """        
        ts.is_type((target, np.ndarray, "target"), (prediction, np.ndarray, "prediction"))
        err = np.where(np.abs(target - prediction) < self._delta, 
                       0.5 * ((target - prediction)**2), 
                       self._delta * np.abs(target - prediction) - 0.5 * (self._delta**2))
        if normalize:
            return err / target
        else:
            return err

class LogCoshError(BaseErrorFunction):
    """Implementation of log-cosh error.
    
    Args:
        None
    """
    
    def __init__(self):
        super().__init__(self)

    def calculate_error(self, target, prediction, normalize=True):
        """Calculates the log-cosh error between a prediction and its target.
        
        Args:
            target (numpy.ndarray): Array of target values
            prediction (numpy.ndarray): Array of predicted values.
            normalize (optional) (bool): Indicates whether or not to normalize the result.
        """
        ts.is_type((target, np.ndarray, "target"), (prediction, np.ndarray, "prediction"))
        err = np.log(np.cosh(prediction - target))
        if normalize:
            return err / target
        else:
            return err

class SquaredError(BaseErrorFunction):
    """Implementation of squared error.
    
    Args:
        None
    """

    def __init__(self):
        super().__init__(self)

    def calculate_error(self, target, prediction, normalize=True):
        """Calculates the squared error between a prediction and its target.
        
        Args:
            target (numpy.ndarray): Array of target values
            prediction (numpy.ndarray): Array of predicted values.
            normalize (optional) (bool): Indicates whether or not to normalize the result.
        """
        ts.is_type((target, np.ndarray, "target"), (prediction, np.ndarray, "prediction"))
        err = (target - prediction)**2
        if normalize:
            return err / target
        else:
            return err
