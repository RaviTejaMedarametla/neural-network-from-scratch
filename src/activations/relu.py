from __future__ import annotations
import numpy as np
from src.layers.base import Layer

class ReLU(Layer):
    def __init__(self) -> None:
        super().__init__()
        self.x: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.x = x
        return np.maximum(0.0, x)

    def backward(self, grad: np.ndarray) -> np.ndarray:
        assert self.x is not None
        g = grad.copy()
        g[self.x <= 0] = 0
        return g
