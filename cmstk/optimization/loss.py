import numpy as np


class BaseLossFunction(object):
    """Representation of generalized loss functions with single initialization and validation.
    
    Args:
        loss_function (function): The underlying loss function.
        reduction_function (function): The underlying reduction function.
    """

    def __init__(self, loss_function, reduction_function):
        if not callable(loss_function):
            raise TypeError("`loss_function` must be callable")
        if not callable(reduction_function):
            raise TypeError("`reduction_function` must be callable")
        self._loss_function = loss_function
        self._reduction_function = reduction_function

    def loss(self, target, actual):
        """Returns the losses as specified by self._loss_function.
        
        Args:
            target (numpy.ndarray or float): Array of target values or singular target value.
            actual (numpy.ndarray or float): Array of actual values or singular actual value.

        Returns:
            numpy.ndarray or float
        """
        if type(target) not in [np.ndarray, float]:
            raise TypeError("`target` must be of type numpy.ndarray or float")
        if type(actual) not in [np.ndarray, float]:
            raise TypeError("`actual` must be of type numpy.ndarray or float")
        if type(target) is not type(actual):
            raise TypeError("`target` and `actual` must both be of type numpy.ndarray or float")
        if type(target) is np.ndarray and type(actual) is np.ndarray:
            if target.shape != actual.shape:
                raise ValueError("`target` and `actual` must have the same shape")
            is_array = True
        else:
            is_array = False

        return self._loss_function(target, actual, is_array)

    def reduction(self, errors):
        """Returns a 1d array of errors reduced row-wise from a 2d array of errors.
        
        Args:
            errors (numpy.ndarray): 2d array of costs.
        
        Returns:
            numpy.ndarray
        """
        if type(errors) is not np.ndarray:
            raise TypeError("`errors` must be of type numpy.ndarray")
        if len(errors.shape) != 2:
            raise ValueError("`errors` must be a 2d array")
        return self._reduction_function(errors)


class MeanAbsoluteError(BaseLossFunction):
    """Implementation of the mean absolute error loss function."""

    def __init__(self):
        super().__init__(self._mean_absolute_loss, self._mean_absolute_reduction)

    @staticmethod
    def _mean_absolute_loss(target, actual, is_array):
        loss = np.absolute(target - actual)
        if is_array:
            loss = loss.mean(axis=1)
            return loss
        else:
            return float(loss)

    @staticmethod
    def _mean_absolute_reduction(errors):
        reduc = np.absolute(errors)
        reduc = reduc.mean(axis=1)
        return reduc


class MeanSquareError(BaseLossFunction):
    """Implementation of the mean square error loss function."""

    def __init__(self):
        super().__init__(self._mean_square_loss, self._mean_square_reduction)

    @staticmethod
    def _mean_square_loss(target, actual, is_array):
        loss = np.square(target - actual)
        if is_array:
            loss = loss.mean(axis=1)
            return loss
        else:
            return float(loss)

    @staticmethod
    def _mean_square_reduction(errors):
        reduc = np.square(errors)
        reduc = reduc.mean(axis=1)
        return reduc
