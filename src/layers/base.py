from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np


class Layer(ABC):
    def __init__(self) -> None:
        self.training = True

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)

    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def backward(self, grad: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def parameters(self) -> list[dict[str, np.ndarray]]:
        return []

    def train(self) -> None:
        self.training = True

    def eval(self) -> None:
        self.training = False

    def to(self, device: str) -> "Layer":
        return self

    def quantize(self, bits: int = 8) -> None:
        return None

    def flops(self, input_shape: tuple[int, ...]) -> int:
        return int(np.prod(input_shape))

    def memory_footprint(self) -> int:
        return 0
