import numpy as np
from src.optimizers.sgd import SGD


def test_sgd_updates_parameter():
    w = np.array([1.0], dtype=np.float32)
    g = np.array([0.5], dtype=np.float32)
    opt = SGD([{"param": w, "grad": g}], lr=0.1)
    opt.step()
    assert w[0] < 1.0
