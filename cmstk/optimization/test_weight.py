import numpy as np
from cmstk.optimization.weight import TargetNormalWeightingScheme, ZNormalWeightingScheme


def test_target_normal_weighting_scheme():
    data = np.random.normal(size=(100, 5))
    targets = np.random.normal(size=(5,))
    scheme = TargetNormalWeightingScheme(targets)
    weights = scheme.weights(data)
    assert weights.shape == (5,)

def test_z_normal_weighting_scheme():
    data = np.random.normal(size=(100, 5))
    scheme = ZNormalWeightingScheme()
    weights = scheme.weights(data)
    assert weights.shape == (5,)