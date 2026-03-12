from __future__ import annotations
import numpy as np
from .base import Layer


class Dropout(Layer):
    def __init__(self, p: float = 0.5) -> None:
        super().__init__()
        self.p = p
        self.mask: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        if not self.training:
            return x
        keep = 1.0 - self.p
        self.mask = (np.random.rand(*x.shape) < keep).astype(np.float32) / keep
        return x * self.mask

    def backward(self, grad: np.ndarray) -> np.ndarray:
        if self.mask is None:
            return grad
        return grad * self.mask
