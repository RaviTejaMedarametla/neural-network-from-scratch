from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np


class Dataset(ABC):
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, index: int):
        raise NotImplementedError


class TensorDataset(Dataset):
    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        self.x = x
        self.y = y

    def __len__(self) -> int:
        return self.x.shape[0]

    def __getitem__(self, index: int):
        return self.x[index], self.y[index]


class MNIST(TensorDataset):
    """Synthetic MNIST-like dataset for offline environments."""
    def __init__(self, n: int = 1024, seed: int = 0) -> None:
        rng = np.random.default_rng(seed)
        x = rng.normal(size=(n, 28 * 28)).astype(np.float32)
        y = rng.integers(0, 10, size=(n,), dtype=np.int64)
        super().__init__(x, y)
