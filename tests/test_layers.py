import numpy as np
from src.layers.dense import Dense
from src.layers.conv import Conv2D


def test_dense_shape():
    x = np.random.randn(5, 4).astype(np.float32)
    d = Dense(4, 3)
    y = d.forward(x)
    assert y.shape == (5, 3)


def test_conv_shape():
    x = np.random.randn(2, 3, 8, 8).astype(np.float32)
    c = Conv2D(3, 4, 3, padding=1)
    y = c.forward(x)
    assert y.shape == (2, 4, 8, 8)
