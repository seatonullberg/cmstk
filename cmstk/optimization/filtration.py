import numpy as np


class BaseFilter(object):
    """Abstract representation of a filter.
    
    Args:
        obj (instance of BaseFilter): A BaseFilter instance used to ensure it has a `filter` method.
    """

    def __init__(self, obj):
        if not isinstance(obj, BaseFilter):
            raise TypeError("`obj` must be an instance of BaseFilter")
        obj_methods = [method_name for method_name in dir(object) if callable(getattr(obj, method_name))]
        if "filter" not in obj_methods:
            raise ValueError("`obj` must implement a method called `filter`")


class ParetoFilter(BaseFilter):
    """Implementation of a Pareto efficiency filter."""

    def __init__(self):
        super().__init__(self)

    def filter(self, arr):
        """Returns a mask of Pareto efficient points.
        
        Args:
            arr (numpy.ndarray): Array of costs.

        Returns:
            numpy.ndarray
        """
        is_efficient = np.ones(arr.shape[0], dtype=bool)
        for i, cost in enumerate(arr):
            if is_efficient[i]:
                is_efficient[is_efficient] = np.any(arr[is_efficient] < cost, axis=1)  # Keep any point with a lower cost
                is_efficient[i] = True  # And keep self
        return is_efficient


class PercentileFilter(BaseFilter):
    """Implementation of a percentile filter."""

    def __init__(self):
        super().__init__(self)

    def filter(self, arr, percentile):
        """Returns a mask of points at or above the given percentile.
        
        Args:
            arr (numpy.ndarray): Array of costs.
            percentile (float): The percentile rank below which observations are excluded.
            - a value of 0.95 would return a mask which exposes the top 5% of performance space.
        
        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


# TODO: may want to create a constraint object rather than use a general dictionary?
# - qoi object keys with max and min value properties
class ConstraintFilter(BaseFilter):
    """Implementation of a quantity of interest based constraint filter."""

    def __init__(self):
        super().__init__(self)

    def filter(self, arr, constraints):
        """Returns a mask of points which satisfy the constraints.
        
        Args:
            arr (numpy.ndarray): Array of costs.
            constraints (dict): Dictionary of constraints by quantity of interest. 

        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


class BaseFilterSet(object):
    """Representation of a generalized combination of filter objects.
    
    Args:
        filters (list of BaseFilter instances): The filters to be combined.
    """

    def __init__(self, filters):
        if type(filters) is not list:
            raise TypeError("`filters` must be of type list")
        for f in filters:
            if not isinstance(f, BaseFilter):
                raise TypeError("all members of `filter` must be instances of type BaseFilter")
        self._filters = filters


class IntersectionalFilterSet(BaseFilterSet):
    """Implementation of a filter set which applies the intersection of all filter masks.
    
    Args:
        filters (list of BaseFilter instances): The filters to be combined.
    """

    def __init__(self, filters)
        super().__init__(filters)


class SequentialFilterSet(BaseFilterSet):
    """Implementation of a filter set which applies its filters in the sequence of their addition.
    
    Args:
        filters (list of BaseFilter instances): The filters to be combined.
    """
    
    def __init__(self, filters):
        super().__init__(filters)
