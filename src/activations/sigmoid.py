from __future__ import annotations
import numpy as np
from src.layers.base import Layer

class Sigmoid(Layer):
    def __init__(self) -> None:
        super().__init__()
        self.y: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.y = 1.0 / (1.0 + np.exp(-x))
        return self.y

    def backward(self, grad: np.ndarray) -> np.ndarray:
        assert self.y is not None
        return grad * self.y * (1.0 - self.y)
