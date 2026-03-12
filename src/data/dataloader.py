from __future__ import annotations
import numpy as np
from .dataset import Dataset


class DataLoader:
    def __init__(self, dataset: Dataset, batch_size: int = 32, shuffle: bool = True, seed: int = 0) -> None:
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.rng = np.random.default_rng(seed)

    def __iter__(self):
        idx = np.arange(len(self.dataset))
        if self.shuffle:
            self.rng.shuffle(idx)
        for start in range(0, len(idx), self.batch_size):
            batch = idx[start:start + self.batch_size]
            xs, ys = zip(*(self.dataset[i] for i in batch))
            yield np.stack(xs), np.array(ys)
