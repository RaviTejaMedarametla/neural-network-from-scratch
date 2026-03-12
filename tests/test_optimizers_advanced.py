import numpy as np

from src.optimizers import AdaBound, AdamW, Nadam


def _single_param():
    w = np.array([1.0], dtype=np.float32)
    g = np.array([0.1], dtype=np.float32)
    return [{"param": w, "grad": g}]


def test_adamw_updates():
    p = _single_param()
    AdamW(p, lr=0.1).step()
    assert p[0]["param"][0] != 1.0


def test_nadam_updates():
    p = _single_param()
    Nadam(p, lr=0.1).step()
    assert p[0]["param"][0] != 1.0


def test_adabound_updates():
    p = _single_param()
    AdaBound(p, lr=0.1).step()
    assert p[0]["param"][0] != 1.0
