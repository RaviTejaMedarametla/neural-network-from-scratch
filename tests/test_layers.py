import numpy as np

from src.layers.conv import Conv2D
from src.layers.dense import Dense


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


def test_conv2d_backward_matches_finite_difference_weight_bias_and_input():
    np.random.seed(0)
    x = np.random.randn(1, 1, 4, 4).astype(np.float32)
    conv = Conv2D(1, 1, 3, stride=1, padding=1, bias=True)

    y = conv.forward(x)
    grad_out = np.random.randn(*y.shape).astype(np.float32)
    dx = conv.backward(grad_out)

    eps = 1e-3

    wi = (0, 0, 1, 1)
    old_w = conv.w[wi]
    conv.w[wi] = old_w + eps
    lp = float(np.sum(conv.forward(x) * grad_out))
    conv.w[wi] = old_w - eps
    lm = float(np.sum(conv.forward(x) * grad_out))
    conv.w[wi] = old_w
    num_dw = (lp - lm) / (2 * eps)
    assert np.isclose(conv.dw[wi], num_dw, rtol=2e-2, atol=2e-2)

    bi = 0
    old_b = conv.b[bi]
    conv.b[bi] = old_b + eps
    lp = float(np.sum(conv.forward(x) * grad_out))
    conv.b[bi] = old_b - eps
    lm = float(np.sum(conv.forward(x) * grad_out))
    conv.b[bi] = old_b
    num_db = (lp - lm) / (2 * eps)
    assert np.isclose(conv.db[bi], num_db, rtol=2e-2, atol=2e-2)

    xi = (0, 0, 2, 2)
    old_x = x[xi]
    x[xi] = old_x + eps
    lp = float(np.sum(conv.forward(x) * grad_out))
    x[xi] = old_x - eps
    lm = float(np.sum(conv.forward(x) * grad_out))
    x[xi] = old_x
    num_dx = (lp - lm) / (2 * eps)
    assert np.isclose(dx[xi], num_dx, rtol=2e-2, atol=2e-2)
