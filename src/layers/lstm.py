from __future__ import annotations
import numpy as np
from .base import Layer


class LSTM(Layer):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.w = np.random.randn(input_size + hidden_size, 4 * hidden_size).astype(np.float32) * 0.05
        self.b = np.zeros((1, 4 * hidden_size), dtype=np.float32)

    def forward(self, x: np.ndarray) -> np.ndarray:
        batch, steps, _ = x.shape
        h = np.zeros((batch, self.hidden_size), dtype=np.float32)
        c = np.zeros_like(h)
        for t in range(steps):
            z = np.concatenate([x[:, t, :], h], axis=1) @ self.w + self.b
            i, f, g, o = np.split(z, 4, axis=1)
            i = 1 / (1 + np.exp(-i))
            f = 1 / (1 + np.exp(-f))
            o = 1 / (1 + np.exp(-o))
            g = np.tanh(g)
            c = f * c + i * g
            h = o * np.tanh(c)
        return h

    def backward(self, grad: np.ndarray) -> np.ndarray:
        return grad
