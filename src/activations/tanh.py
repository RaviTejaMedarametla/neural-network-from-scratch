from __future__ import annotations
import numpy as np
from src.layers.base import Layer

class Tanh(Layer):
    def __init__(self) -> None:
        super().__init__()
        self.y: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.y = np.tanh(x)
        return self.y

    def backward(self, grad: np.ndarray) -> np.ndarray:
        assert self.y is not None
        return grad * (1 - self.y**2)
