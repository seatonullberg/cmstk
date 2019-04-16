import numpy as np


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


class ParetoFilter(BaseFilter):
    """Implementation of a Pareto efficiency filter.
    
    Args:
        arr (numpy.ndarray): Array of costs.
    """

    def __init__(self, arr):
        super().__init__(self)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type np.ndarray")
        self._arr = arr

    def filter(self):
        """Returns a mask of Pareto efficient points.

        Returns:
            numpy.ndarray
        """
        is_efficient = np.ones(self._arr.shape[0], dtype=bool)
        for i, cost in enumerate(arr):
            if is_efficient[i]:
                is_efficient[is_efficient] = np.any(self._arr[is_efficient] < cost, axis=1)  # Keep any point with a lower cost
                is_efficient[i] = True  # And keep self
        return is_efficient


class PercentileFilter(BaseFilter):
    """Implementation of a percentile filter.
    
    Args:
        arr (numpy.ndarray): Array of costs.
        percentile (float): The percentile rank below which observations are excluded.
    """

    def __init__(self, arr, percentile):
        super().__init__(self)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type numpy.ndarray")
        if type(percentile) is not float:
            raise TypeError("`percentile` must be of type float")
        self._arr = arr
        self._percentile = percentile

    def filter(self):
        """Returns a mask of points at or above the given percentile.
        
        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


# TODO: may want to create a constraint object rather than use a general dictionary?
# - qoi object keys with max and min value properties
class ConstraintFilter(BaseFilter):
    """Implementation of a quantity of interest based constraint filter.
    
    Args:
        arr (numpy.ndarray): Array of costs.
        constraints (dict): Dictionary of constraints by qoi
    """

    def __init__(self, arr, constraints):
        super().__init__(self)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type numpy.ndarray")
        if type(constraints) is not dict:
            raise TypeError("`constraints` must be of type dict")
        self._arr = arr
        self._constraints = constraints


    def filter(self):
        """Returns a mask of points which satisfy the constraints.

        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


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

    def __init__(self)
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
