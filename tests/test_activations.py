import numpy as np
from src.activations.relu import ReLU


def test_relu_backward_masking():
    x = np.array([[-1.0, 2.0]], dtype=np.float32)
    relu = ReLU()
    relu.forward(x)
    g = relu.backward(np.ones_like(x))
    assert np.allclose(g, np.array([[0.0, 1.0]], dtype=np.float32))
