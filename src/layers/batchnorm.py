from __future__ import annotations
import numpy as np
from .base import Layer


class BatchNorm(Layer):
    def __init__(self, num_features: int, momentum: float = 0.1, eps: float = 1e-5) -> None:
        super().__init__()
        self.gamma = np.ones((1, num_features), dtype=np.float32)
        self.beta = np.zeros((1, num_features), dtype=np.float32)
        self.running_mean = np.zeros((1, num_features), dtype=np.float32)
        self.running_var = np.ones((1, num_features), dtype=np.float32)
        self.momentum = momentum
        self.eps = eps
        self.cache: tuple[np.ndarray, np.ndarray, np.ndarray] | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        if self.training:
            mean = x.mean(axis=0, keepdims=True)
            var = x.var(axis=0, keepdims=True)
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * mean
            self.running_var = (1 - self.momentum) * self.running_var + self.momentum * var
        else:
            mean, var = self.running_mean, self.running_var
        xhat = (x - mean) / np.sqrt(var + self.eps)
        self.cache = (x, mean, var)
        return self.gamma * xhat + self.beta

    def backward(self, grad: np.ndarray) -> np.ndarray:
        return grad
