from __future__ import annotations

import numpy as np


class WeightedSampler:
    """Sample dataset indices according to example weights."""

    def __init__(self, weights: np.ndarray, num_samples: int, seed: int = 0) -> None:
        self.weights = weights / np.sum(weights)
        self.num_samples = num_samples
        self.rng = np.random.default_rng(seed)

    def sample(self) -> np.ndarray:
        idx = np.arange(self.weights.shape[0])
        return self.rng.choice(idx, size=self.num_samples, replace=True, p=self.weights)
