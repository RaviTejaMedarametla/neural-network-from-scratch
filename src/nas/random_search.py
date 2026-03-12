from __future__ import annotations

import numpy as np

from .search_space import Architecture, SearchSpace


class RandomSearchNAS:
    """Random NAS with optional hardware-constrained scoring."""

    def __init__(self, search_space: SearchSpace, trials: int = 50, seed: int = 0) -> None:
        self.search_space = search_space
        self.trials = trials
        self.rng = np.random.default_rng(seed)

    def search(self, fitness_fn) -> tuple[Architecture, float]:
        best_arch: Architecture | None = None
        best_score = -1e18
        for _ in range(self.trials):
            arch = Architecture(self.search_space.sample(self.rng))
            score = float(fitness_fn(arch))
            if score > best_score:
                best_score = score
                best_arch = arch
        if best_arch is None:
            raise RuntimeError("No architecture sampled")
        return best_arch, best_score
