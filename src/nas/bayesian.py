from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np

from .search_space import Architecture, SearchSpace


@dataclass
class GPHyperParams:
    """Hyperparameters for the lightweight Gaussian Process surrogate."""

    length_scale: float = 1.0
    signal_variance: float = 1.0
    noise_variance: float = 1e-4


class BayesianNAS:
    """Bayesian optimization NAS with a small RBF-kernel GP surrogate.

    Notes:
        This implementation intentionally targets small architecture spaces and
        lightweight experiments. It uses expected improvement as acquisition.
    """

    def __init__(
        self,
        search_space: SearchSpace,
        warmup: int = 16,
        iterations: int = 24,
        candidates_per_iter: int = 64,
        seed: int = 0,
        gp_params: GPHyperParams | None = None,
    ) -> None:
        self.search_space = search_space
        self.warmup = warmup
        self.iterations = iterations
        self.candidates_per_iter = candidates_per_iter
        self.rng = np.random.default_rng(seed)
        self.gp = gp_params or GPHyperParams()

    def _featurize(self, arch: Architecture) -> np.ndarray:
        ops = [op.name for op in arch.layers]
        uniq = sorted({op.name for op in self.search_space.operations})

        # Bag-of-ops + position-aware histogram.
        bag = np.zeros((len(uniq),), dtype=np.float64)
        pos = np.zeros((len(uniq), len(ops)), dtype=np.float64)
        for i, op in enumerate(ops):
            idx = uniq.index(op)
            bag[idx] += 1.0
            pos[idx, i] = 1.0

        bag = bag / max(len(ops), 1)
        return np.concatenate([bag, pos.reshape(-1)])

    def _rbf_kernel(self, xa: np.ndarray, xb: np.ndarray) -> np.ndarray:
        ls = max(self.gp.length_scale, 1e-9)
        sq_a = np.sum(xa * xa, axis=1, keepdims=True)
        sq_b = np.sum(xb * xb, axis=1, keepdims=True).T
        sqdist = np.maximum(sq_a + sq_b - 2.0 * xa @ xb.T, 0.0)
        return self.gp.signal_variance * np.exp(-0.5 * sqdist / (ls * ls))

    def _fit_gp(self, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        k_xx = self._rbf_kernel(x, x)
        k_xx += np.eye(k_xx.shape[0]) * self.gp.noise_variance
        # Cholesky for stability.
        l = np.linalg.cholesky(k_xx + 1e-9 * np.eye(k_xx.shape[0]))
        alpha = np.linalg.solve(l.T, np.linalg.solve(l, y))
        return l, alpha

    def _predict_gp(self, x_train: np.ndarray, l: np.ndarray, alpha: np.ndarray, x_star: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        k_xs = self._rbf_kernel(x_train, x_star)
        mean = k_xs.T @ alpha

        v = np.linalg.solve(l, k_xs)
        k_ss_diag = np.diag(self._rbf_kernel(x_star, x_star))
        var = np.maximum(k_ss_diag - np.sum(v * v, axis=0), 1e-12)
        return mean, var

    def _expected_improvement(self, mean: np.ndarray, var: np.ndarray, best: float, xi: float = 0.01) -> np.ndarray:
        sigma = np.sqrt(np.maximum(var, 1e-12))
        improve = mean - best - xi
        z = improve / sigma

        # Normal CDF/PDF via erf.
        cdf = 0.5 * (1.0 + np.vectorize(math.erf)(z / np.sqrt(2.0)))
        pdf = (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(-0.5 * z * z)
        ei = improve * cdf + sigma * pdf
        return np.maximum(ei, 0.0)

    def search(self, fitness_fn: Callable[[Architecture], float]) -> tuple[Architecture, float]:
        observed_arch: list[Architecture] = []
        observed_y: list[float] = []

        # Warmup random evaluations.
        for _ in range(self.warmup):
            arch = Architecture(self.search_space.sample(self.rng))
            observed_arch.append(arch)
            observed_y.append(float(fitness_fn(arch)))

        best_idx = int(np.argmax(observed_y))
        best_arch = observed_arch[best_idx]
        best_score = float(observed_y[best_idx])

        for _ in range(self.iterations):
            x_train = np.stack([self._featurize(a) for a in observed_arch])
            y_train = np.array(observed_y, dtype=np.float64)

            l, alpha = self._fit_gp(x_train, y_train)

            pool = [Architecture(self.search_space.sample(self.rng)) for _ in range(self.candidates_per_iter)]
            x_pool = np.stack([self._featurize(a) for a in pool])
            mean, var = self._predict_gp(x_train, l, alpha, x_pool)
            ei = self._expected_improvement(mean, var, best_score)

            chosen = pool[int(np.argmax(ei))]
            score = float(fitness_fn(chosen))
            observed_arch.append(chosen)
            observed_y.append(score)

            if score > best_score:
                best_arch = chosen
                best_score = score

        return best_arch, best_score


# Backward-compatible alias retained for existing imports.
SurrogateNAS = BayesianNAS
