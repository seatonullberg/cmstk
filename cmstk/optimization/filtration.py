import type_sanity as ts
import numpy as np


class BaseFilter(object):
    """Abstract representation of a filter.
    
    Args:
        obj (instance of BaseFilter): A BaseFilter instance used to ensure it has a `filter` method.
    """

    def __init__(self, obj):
        ts.is_instance((obj, BaseFilter, "obj"))
        ts.implements((obj, "filter", "obj"))


# TODO: may want to create a constraint object rather than use a general dictionary?
# - qoi object keys with max and min value properties
class ConstraintFilter(BaseFilter):
    """Implementation of a quantity of interest based constraint filter.
    
    Args:
        arr (numpy.ndarray): Array of costs.
        constraints (dict): Dictionary of constraints by qoi.
    """

    def __init__(self, constraints):
        super().__init__(self)
        ts.is_type((constraints, dict, "constraints"))
        self._constraints = constraints

    def filter(self, arr):
        """Returns a mask of points which satisfy the constraints.

        Args:
            arr (numpy.ndarray): Array of costs

        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


class PercentileFilter(BaseFilter):
    """Implementation of a filter which scores samples as a row-wise summation and applies a percentile constraint.
    
    Args:
        percentile (float): The percentile value to accept.
    """

    def __init__(self, percentile):
        super().__init__(self)
        ts.is_type((percentile, float, "percentile"))
        if not 0.0 < percentile < 100.0:
            raise ValueError("`percentile` must be between 0.0 and 100.0")
        self._percentile = percentile

    def filter(self, arr):
        """Returns a mask of points with acceptable loss.
        
        Args:
            arr (numpy.ndarray): Array of costs.

        Returns:
            numpy.ndarray
        """
        ts.is_type((arr, np.ndarray, "arr"))
        costs = np.sum(arr, axis=1)
        percentile_val = np.percentile(costs, self._percentile)
        efficient_indices = costs <= percentile_val
        return efficient_indices


class ParetoFilter(BaseFilter):
    """Implementation of a Pareto efficiency filter.
    
    Args:
        None
    """

    def __init__(self):
        super().__init__(self)

    def filter(self, arr):
        """Returns a mask of Pareto efficient points.

        Args:
            arr (numpy.ndarray): Array of costs.

        Returns:
            numpy.ndarray
        """
        ts.is_type((arr, np.ndarray, "arr"))
        is_efficient = np.ones(arr.shape[0], dtype=bool)
        for i, cost in enumerate(arr):
            if is_efficient[i]:
                is_efficient[is_efficient] = np.any(arr[is_efficient] < cost, axis=1)  # Keep any point with a lower cost
                is_efficient[i] = True  # And keep self
        return is_efficient


class BaseFilterSet(object):
    """Representation of a generalized combination of filter objects.
    
    Args:
        obj (instance of BaseFilterSet): A BaseFilterSet instance used to ensure it has an `apply` method.
    """

    def __init__(self, obj):
        ts.implements((obj, "apply", "obj"))
        self._filters = []

    def add_filter(self, f):
        ts.is_instance((f, BaseFilter, "f"))
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
        masks = [f.filter(arr) for f in self._filters]
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
        # apply masks in sequence
        for f in self._filters:
            mask = f.filter(arr)
            arr = arr[mask]
        return arr
