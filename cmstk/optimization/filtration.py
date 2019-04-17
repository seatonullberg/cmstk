from cmstk.optimization.loss import BaseLossFunction
import numpy as np
from sklearn.preprocessing import StandardScaler


class BaseFilter(object):
    """Abstract representation of a filter.
    
    Args:
        obj (instance of BaseFilter): A BaseFilter instance used to ensure it has a `filter` method.
    """

    def __init__(self, obj):
        if not isinstance(obj, BaseFilter):
            raise TypeError("`obj` must be an instance of BaseFilter")
        obj_methods = [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]
        if "filter" not in obj_methods:
            raise ValueError("`obj` must implement a method called `filter`")
        self._scaler = StandardScaler()  # store this for faster use

    def normalize(self, arr):
        """Normalize features by removing the mean and scaling to unit variance.
        
        Args:
            arr (numpy.ndarray): Array to be normalized.

        Returns:
            numpy.ndarray
        """
        return self._scaler.fit_transform(arr)


# TODO: may want to create a constraint object rather than use a general dictionary?
# - qoi object keys with max and min value properties
class ConstraintFilter(BaseFilter):
    """Implementation of a quantity of interest based constraint filter.
    
    Args:
        arr (numpy.ndarray): Array of costs.
        constraints (dict): Dictionary of constraints by qoi.
        normalize (optional) (bool): Normalize the array of costs if True.
        - True by default
    """

    def __init__(self, arr, constraints, normalize=True):
        super().__init__(self)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type numpy.ndarray")
        if type(constraints) is not dict:
            raise TypeError("`constraints` must be of type dict")
        self._arr = arr
        self._constraints = constraints
        self._normalize = normalize


    def filter(self):
        """Returns a mask of points which satisfy the constraints.

        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


class LossFunctionFilter(BaseFilter):
    """Implementation of a filter which takes an arbitrary loss function.
    
    Args:
        arr (numpy.ndarray): Array of costs.
        loss_function (instance of BaseLossFunction): The loss function to apply.
        normalize (optional) (bool): Normalize the array of costs if True.
        - True by default
    """

    def __init__(self, arr, loss_function, normalize=True):
        super().__init__(self)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type numpy.ndarray")
        if not isinstance(loss_function, BaseLossFunction):
            raise TypeError("`loss_function` must be an instance of type BaseLossFunction")
        self._arr = arr
        self._loss_function = loss_function
        self._normalize = normalize

    def filter(self):
        """Returns a mask of points with acceptable loss.
        
        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


class ParetoFilter(BaseFilter):
    """Implementation of a Pareto efficiency filter.
    
    Args:
        arr (numpy.ndarray): Array of costs.
        normalize (optional) (bool): Normalize the array of costs if True.
        - True by default
    """

    def __init__(self, arr, normalize=True):
        super().__init__(self)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type numpy.ndarray")
        self._arr = arr
        self._normalize = normalize

    def filter(self):
        """Returns a mask of Pareto efficient points.

        Returns:
            numpy.ndarray
        """
        if self._normalize:
            self._arr = self.normalize(self._arr)

        is_efficient = np.ones(self._arr.shape[0], dtype=bool)
        for i, cost in enumerate(self._arr):
            if is_efficient[i]:
                is_efficient[is_efficient] = np.any(self._arr[is_efficient] < cost, axis=1)  # Keep any point with a lower cost
                is_efficient[i] = True  # And keep self
        return is_efficient


class PercentileFilter(BaseFilter):
    """Implementation of a percentile filter.
    
    Args:
        arr (numpy.ndarray): Array of costs.
        percentile (float): The percentile rank below which observations are excluded.
        normalize (optional) (bool): Normalize the array of costs if True.
        - True by default
    """

    def __init__(self, arr, percentile, normalize=True):
        super().__init__(self)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type numpy.ndarray")
        if type(percentile) is not float:
            raise TypeError("`percentile` must be of type float")
        self._arr = arr
        self._percentile = percentile
        self._normalize = normalize

    def filter(self):
        """Returns a mask of points at or above the given percentile.
        
        Returns:
            numpy.ndarray
        """
        if self._normalize:
            self._arr = self.normalize(self._arr)

        abs_arr = abs(self._arr)  # use absolutes for effective <= comparison
        row_summations = np.sum(abs_arr, axis=1)
        percentile_val = np.percentile(row_summations, self._percentile)
        efficient_indices = row_summations <= percentile_val
        return efficient_indices


class BaseFilterSet(object):
    """Representation of a generalized combination of filter objects.
    
    Args:
        obj (instance of BaseFilterSet): A BaseFilterSet instance used to ensure it has an `apply` method.
    """

    def __init__(self, obj):
        obj_methods = [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]
        if "apply" not in obj_methods:
            raise ValueError("`obj` must implement a method called `apply`")
        self._filters = []

    def add_filter(self, f):
        if not isinstance(f, BaseFilter):
            raise TypeError("`f` must be an instance of type BaseFilter")
        self._filters.append(f)


class IntersectionalFilterSet(BaseFilterSet):
    """Implementation of a filter set which applies the intersection of all filter masks simultaneously."""

    def __init__(self):
        super().__init__(self)

    def apply(self, arr):
        """Returns the filtered results.
        
        Args:
            arr (numpy.ndarray): Array of values to be filtered.

        Returns:
            numpy.ndarray
            - The same array, filtered.
        """
        masks = [f.filter() for f in self._filters]
        if len(masks) == 0:
            return arr  # return the unfiltered array
        if len(masks) == 1:
            return arr[masks[0]]
        # apply intersection of all masks
        current_mask = masks[0]
        for m in masks[1:]:
            current_mask = np.logical_and(current_mask, m)
        return arr[current_mask]


class SequentialFilterSet(BaseFilterSet):
    """Implementation of a filter set which applies all filter masks in the sequence of their addition."""
    
    def __init__(self):
        super().__init__(self)

    def apply(self, arr):
        """Returns the filtered results.
        
        Args:
            arr (numpy.ndarray): Array of values to be filtered.

        Returns:
            numpy.ndarray
            - The same array, filtered.
        """
        masks = [f.filter() for f in self._filters]
        if len(masks) == 0:
            return arr  # return the unfiltered array
        if len(masks) == 1:
            return arr[masks[0]]
        # apply masks in sequence
        for m in masks:
            arr = arr[m]
        return arr
