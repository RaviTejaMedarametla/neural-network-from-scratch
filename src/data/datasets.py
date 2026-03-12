from __future__ import annotations

import numpy as np

from .dataset import Dataset, TensorDataset


class CIFAR10(TensorDataset):
    """Synthetic CIFAR-10 fallback dataset for offline tests and demos."""

    def __init__(self, n: int = 1024, seed: int = 123, flatten: bool = False) -> None:
        rng = np.random.default_rng(seed)
        x = rng.uniform(0, 1, size=(n, 32, 32, 3)).astype(np.float32)
        y = rng.integers(0, 10, size=(n,), dtype=np.int64)
        if flatten:
            x = x.reshape(n, -1)
        super().__init__(x, y)


class FashionMNIST(TensorDataset):
    """Synthetic FashionMNIST fallback dataset for offline tests and demos."""

    def __init__(self, n: int = 1024, seed: int = 124, flatten: bool = True) -> None:
        rng = np.random.default_rng(seed)
        x = rng.normal(0, 1, size=(n, 28, 28, 1)).astype(np.float32)
        y = rng.integers(0, 10, size=(n,), dtype=np.int64)
        if flatten:
            x = x.reshape(n, -1)
        super().__init__(x, y)


class TinyLanguageModeling(Dataset):
    """Tiny synthetic integer-token dataset for embedding/transformer examples."""

    def __init__(self, n: int = 512, seq_len: int = 16, vocab_size: int = 128, seed: int = 7) -> None:
        self.rng = np.random.default_rng(seed)
        self.tokens = self.rng.integers(0, vocab_size, size=(n, seq_len), dtype=np.int64)
        self.targets = self.rng.integers(0, vocab_size, size=(n,), dtype=np.int64)

    def __len__(self) -> int:
        return self.tokens.shape[0]

    def __getitem__(self, index: int):
        return self.tokens[index], self.targets[index]
