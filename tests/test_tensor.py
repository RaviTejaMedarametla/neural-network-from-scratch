import numpy as np
from src.tensor.tensor import Tensor


def test_tensor_add_backward():
    a = Tensor(np.array([1.0, 2.0]), requires_grad=True)
    b = Tensor(np.array([3.0, 4.0]), requires_grad=True)
    c = (a + b).sum()
    c.backward()
    assert np.allclose(a.grad, np.ones_like(a.data))
    assert np.allclose(b.grad, np.ones_like(b.data))
