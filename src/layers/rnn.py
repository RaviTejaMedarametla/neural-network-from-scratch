from __future__ import annotations
import numpy as np
from .base import Layer


class RNN(Layer):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.wxh = np.random.randn(input_size, hidden_size).astype(np.float32) * 0.1
        self.whh = np.random.randn(hidden_size, hidden_size).astype(np.float32) * 0.1
        self.b = np.zeros((1, hidden_size), dtype=np.float32)
        self.cache: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []

    def forward(self, x: np.ndarray) -> np.ndarray:
        h = np.zeros((x.shape[0], self.hidden_size), dtype=np.float32)
        self.cache.clear()
        for t in range(x.shape[1]):
            xt = x[:, t, :]
            h = np.tanh(xt @ self.wxh + h @ self.whh + self.b)
            self.cache.append((xt, h.copy(), h.copy()))
        return h

    def backward(self, grad: np.ndarray) -> np.ndarray:
        return grad
