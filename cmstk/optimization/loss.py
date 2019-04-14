import numpy as np

# TODO: double check which axis these operation should occur on

class LossFunction(object):
    """Representation of generalized loss functions with single initialization and validation.
    
    Args:
        evaluation_function (function): The underlying loss function.
    """

    def __init__(self, evaluation_function):
        if not callable(evaluation_function):
            raise TypeError("`evaluation_function` must be callable")
        self._evaluation_function = evaluation_function

    def loss(self, targets, actuals):
        """Calculates the loss as specified by self._evaluation_function.
        
        Args:
            targets (np.ndarray): Array of target values.
            actuals (np.ndarray): Array of actual values.

        Returns:
            np.ndarray
        """
        if type(targets) is not np.ndarray:
            raise TypeError("`targets` must be of type np.ndarray")
        if type(actuals) is not np.ndarray:
            raise TypeError("`actuals` must be of type np.ndarray")
        return self._evaluation_function(targets, actuals)


class LogCoshError(LossFunction):
    """Implementation of the log cosh loss function."""

    def __init__(self):
        super().__init__(self._log_cosh_error)

    @staticmethod
    def _log_cosh_error(targets, actuals):
        loss = np.log(np.cosh(actuals - targets))
        return np.sum(loss)


class MeanAbsoluteError(LossFunction):
    """Implementation of the mean absolute error loss function."""

    def __init__(self):
        super().__init__(self._mean_absolute_error)

    @staticmethod
    def _mean_absolute_error(targets, actuals):
        return (np.absolute(targets - actuals)).mean(axis=0)


class MeanSquareError(LossFunction):
    """Implementation of the mean square error loss function."""

    def __init__(self):
        super().__init__(self._mean_square_error)

    @staticmethod
    def _mean_square_error(targets, actuals):
        return (np.square(targets - actuals)).mean(axis=0)
