from cmstk.optimization.sampling import GaussianSampler, KDESampler, UniformSampler
import numpy as np


def test_gaussian_sampler():
    n_samples = 10
    mean = np.array([0.0, 0.0, 0.0])
    stdev = np.array([1.0, 1.0, 1.0])
    gs = GaussianSampler(n_samples, mean, stdev)
    samples = gs.sample()
    assert type(samples) is np.ndarray
    assert samples.shape[0] == 10
    assert samples.shape[1] == 3

def test_kde_sampler():
    n_samples = 10
    arr = np.random.normal(size=(100, 3))
    bandwidth = 0.1  # completely arbitrary
    ks = KDESampler(n_samples, arr, bandwidth)
    samples = ks.sample()
    assert type(samples) is np.ndarray
    assert samples.shape[0] == 10
    assert samples.shape[1] == 3

def test_uniform_sampler():
    n_samples = 10
    low = np.array([0.0, 0.0, 0.0])
    high = np.array([1.0, 1.0, 1.0])
    us = UniformSampler(n_samples, low, high)
    samples = us.sample()
    assert type(samples) is np.ndarray
    assert samples.shape[0] == 10
    assert samples.shape[1] == 3
    assert samples.min() >= 0
    assert samples.max() <= 1