import numpy as np


def custom_uniform(n_in, n_out, rng=None, dtype=np.float32):
    limit = np.sqrt(6.0 / (n_in + n_out))
    sampler = np.random if rng is None else rng
    weights = sampler.uniform(-limit, limit, (n_in, n_out))
    return weights.astype(dtype)


class DenseLayer:
    def __init__(self, n_in, n_out, rng=None, dtype=np.float32):
        self.weights = custom_uniform(n_in, n_out, rng=rng, dtype=dtype)
        self.bias = np.zeros((1, n_out), dtype=dtype)
        self.input_cache = None
        self.z_cache = None

    def forward(self, x, weights=None, bias=None):
        w = self.weights if weights is None else weights
        b = self.bias if bias is None else bias
        self.input_cache = x
        self.z_cache = x @ w + b
        return self.z_cache

    def backward(self, delta, l2_lambda=0.0):
        batch_size = self.input_cache.shape[0]
        grad_w = (self.input_cache.T @ delta) / batch_size
        if l2_lambda > 0:
            grad_w = grad_w + l2_lambda * self.weights
        grad_b = np.sum(delta, axis=0, keepdims=True) / batch_size
        grad_input = delta @ self.weights.T
        return grad_input, grad_w, grad_b
