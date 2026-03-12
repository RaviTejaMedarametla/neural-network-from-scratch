from __future__ import annotations
import numpy as np
from src.layers.base import Layer

class Softmax(Layer):
    def forward(self, x: np.ndarray) -> np.ndarray:
        shifted = x - np.max(x, axis=1, keepdims=True)
        ex = np.exp(shifted)
        return ex / np.sum(ex, axis=1, keepdims=True)

    def backward(self, grad: np.ndarray) -> np.ndarray:
        return grad
