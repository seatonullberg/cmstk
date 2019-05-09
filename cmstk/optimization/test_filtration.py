from cmstk.optimization.filtration import ConstraintFilter, PercentileFilter, ParetoFilter
from cmstk.optimization.filtration import IntersectionalFilterSet, SequentialFilterSet
import numpy as np
import pytest


def test_constraint_filter():
    # tests the CosntraintFilter individually
    data = np.random.normal(size=(100, 3))
    with pytest.raises(NotImplementedError):
        cf = ConstraintFilter({})
        cf.filter(data)    

def test_percentile_filter():
    data = np.random.normal(size=(100,3))
    pf = PercentileFilter(5.0)
    mask = pf.filter(data)
    filtered_data = data[mask]
    assert 4 <= filtered_data.shape[0] <= 6  # save 5%

def test_pareto_filter():
    # tests the ParetoFilter individually
    data = np.random.normal(size=(100, 3))
    pf = ParetoFilter()
    mask = pf.filter(data)
    filtered_data = data[mask]
    assert filtered_data.shape[0] < data.shape[0]  # not sure how else to test this

def test_intersectional_filter_set():
    # tests simple IntersectionalFilterSet implementation
    data = np.random.normal(size=(1000, 3))
    pareto_filter = ParetoFilter()
    percentile_filter = PercentileFilter(95.0)
    ifs = IntersectionalFilterSet()
    ifs.add_filter(percentile_filter)  # order irrelevant
    ifs.add_filter(pareto_filter)  # order irrelevant
    result = ifs.apply(data)
    assert result.shape[0] < data.shape[0]  # it did some filtering

def test_intersectional_filter_set_one_filter():
    # tests IntersectionalFilterSet with only one filter
    data = np.random.normal(size=(1000, 3))
    percentile_filter = PercentileFilter(95.0)
    ifs = IntersectionalFilterSet()
    ifs.add_filter(percentile_filter)
    result = ifs.apply(data)
    assert 949 <= result.shape[0] <= 951  # 95 percentile

def test_intersectional_filter_set_no_filters():
    # tests IntersectionalFilterSet without filters added
    data = np.random.normal(size=(1000, 3))
    ifs = IntersectionalFilterSet()
    result = ifs.apply(data)
    assert result.shape[0] == data.shape[0]  # no filtering 

def test_sequential_filter_set():
    # tests simple SequentialFilterSet implementation
    data = np.random.normal(size=(1000, 3))
    pareto_filter = ParetoFilter()
    percentile_filter = PercentileFilter(95.0)
    sfs = SequentialFilterSet()
    sfs.add_filter(percentile_filter)  # remove lowest 5% first
    sfs.add_filter(pareto_filter)  # calculate pareto front of that result
    result = sfs.apply(data)
    assert result.shape[0] < data.shape[0]  # it did some filtering

def test_sequential_filter_set_one_filter():
    # tests SequentialFilterSet with only one filter
    data = np.random.normal(size=(1000, 3))
    percentile_filter = PercentileFilter(95.0)
    sfs = SequentialFilterSet()
    sfs.add_filter(percentile_filter)
    result = sfs.apply(data)
    assert 949 <= result.shape[0] <= 951 # 95 percentile

def test_sequential_filter_set_no_filters():
    # tests SequentialFilterSet without filters added
    data = np.random.normal(size=(1000, 3))
    sfs = SequentialFilterSet()
    result = sfs.apply(data)
    assert result.shape[0] == data.shape[0]  # no filtering 
