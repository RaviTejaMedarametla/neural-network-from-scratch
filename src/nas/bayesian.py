from __future__ import annotations

import numpy as np

from .search_space import Architecture, SearchSpace


class SurrogateNAS:
    """Lightweight surrogate NAS (random features + linear regressor)."""

    def __init__(self, search_space: SearchSpace, warmup: int = 20, iterations: int = 40, seed: int = 0) -> None:
        self.search_space = search_space
        self.warmup = warmup
        self.iterations = iterations
        self.rng = np.random.default_rng(seed)

    def _featurize(self, arch: Architecture) -> np.ndarray:
        ops = [op.name for op in arch.layers]
        uniq = sorted({op.name for op in self.search_space.operations})
        feats = np.zeros((len(ops), len(uniq)), dtype=np.float64)
        for i, op in enumerate(ops):
            feats[i, uniq.index(op)] = 1.0
        return feats.mean(axis=0)

    def search(self, fitness_fn) -> tuple[Architecture, float]:
        candidates: list[Architecture] = []
        y: list[float] = []
        for _ in range(self.warmup):
            a = Architecture(self.search_space.sample(self.rng))
            candidates.append(a)
            y.append(float(fitness_fn(a)))

        X = np.stack([self._featurize(a) for a in candidates])
        w = np.linalg.pinv(X) @ np.array(y)

        best_idx = int(np.argmax(y))
        best_arch, best_score = candidates[best_idx], y[best_idx]

        for _ in range(self.iterations):
            pool = [Architecture(self.search_space.sample(self.rng)) for _ in range(32)]
            pool_x = np.stack([self._featurize(a) for a in pool])
            pred = pool_x @ w
            chosen = pool[int(np.argmax(pred))]
            score = float(fitness_fn(chosen))

            candidates.append(chosen)
            y.append(score)
            X = np.stack([self._featurize(a) for a in candidates])
            w = np.linalg.pinv(X) @ np.array(y)
            if score > best_score:
                best_arch, best_score = chosen, score

        return best_arch, float(best_score)
