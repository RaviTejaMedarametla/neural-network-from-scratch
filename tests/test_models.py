import numpy as np
from src.layers.dense import Dense
from src.models.sequential import Sequential


def test_sequential_forward():
    model = Sequential([Dense(4, 8), Dense(8, 2)])
    x = np.random.randn(3, 4).astype(np.float32)
    y = model.forward(x)
    assert y.shape == (3, 2)
