from __future__ import annotations
import numpy as np
from src.layers.base import Layer

class LeakyReLU(Layer):
    def __init__(self, slope: float = 0.01) -> None:
        super().__init__()
        self.slope = slope
        self.x: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.x = x
        return np.where(x > 0, x, self.slope * x)

    def backward(self, grad: np.ndarray) -> np.ndarray:
        assert self.x is not None
        return grad * np.where(self.x > 0, 1.0, self.slope)
