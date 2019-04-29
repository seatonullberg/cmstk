import type_sanity as ts
from cmstk.optimization.loss import BaseLossFunction
import numpy as np
from sklearn.preprocessing import StandardScaler


class BaseFilter(object):
    """Abstract representation of a filter.
    
    Args:
        obj (instance of BaseFilter): A BaseFilter instance used to ensure it has a `filter` method.
    """

    def __init__(self, obj):
        ts.is_instance((obj, BaseFilter, "obj"))
        ts.implements((obj, "filter", "obj"))
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

    def __init__(self, constraints, normalize=True):
        super().__init__(self)
        ts.is_type((constraints, dict, "constraints"))
        self._constraints = constraints
        self._normalize = normalize

    def filter(self, arr):
        """Returns a mask of points which satisfy the constraints.

        Args:
            arr (numpy.ndarray): Array of costs

        Returns:
            numpy.ndarray
        """
        raise NotImplementedError


class LossFunctionFilter(BaseFilter):
    """Implementation of a filter which takes an arbitrary loss function.
    
    Args:
        loss_function (instance of BaseLossFunction): The loss function to apply.
        normalize (optional) (bool): Normalize the array of costs if True.
        - True by default
    """

    def __init__(self, loss_function, percentile, normalize=True):
        super().__init__(self)
        ts.is_instance((loss_function, BaseLossFunction, "loss_function"))
        ts.is_type((percentile, float, "percentile"))
        if not 0.0 < percentile < 100.0:
            raise ValueError("`percentile` must be between 0.0 and 100.0")
        self._loss_function = loss_function
        self._percentile = percentile
        self._normalize = normalize

    def filter(self, arr):
        """Returns a mask of points with acceptable loss.
        
        Args:
            arr (numpy.ndarray): Array of costs.

        Returns:
            numpy.ndarray
        """
        ts.is_type((arr, np.ndarray, "arr"))
        if self._normalize:
            arr = self.normalize(arr)

        reduced_arr = self._loss_function.reduction(arr)  # use loss function to reduce each row to a scalar
        percentile_val = np.percentile(reduced_arr, self._percentile)
        efficient_indices = reduced_arr <= percentile_val
        return efficient_indices


class ParetoFilter(BaseFilter):
    """Implementation of a Pareto efficiency filter.
    
    Args:
        normalize (optional) (bool): Normalize the array of costs if True.
        - True by default
    """

    def __init__(self, normalize=True):
        super().__init__(self)
        self._normalize = normalize

    def filter(self, arr):
        """Returns a mask of Pareto efficient points.

        Args:
            arr (numpy.ndarray): Array of costs.

        Returns:
            numpy.ndarray
        """
        if self._normalize:
            arr = self.normalize(arr)

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
