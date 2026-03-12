from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class Dataset:
    x_train: np.ndarray
    y_train: np.ndarray
    x_val: np.ndarray
    y_val: np.ndarray


class SyntheticHardwareDataset:
    """
    Synthetic dataset for hardware-aware representation learning.

    Features emulate counters and workload descriptors:
    - arithmetic intensity
    - memory locality
    - tile shape descriptors
    - occupancy and pipeline stalls
    - reuse distances

    Labels indicate best architecture class for a workload.
    """

    def __init__(self, input_dim: int, classes: int, seed: int = 7):
        self.input_dim = input_dim
        self.classes = classes
        self.rng = np.random.default_rng(seed)

    def _latent_kernel(self, n: int) -> np.ndarray:
        g = self.rng.normal(size=(n, self.input_dim))
        transformed = np.empty_like(g, dtype=np.float32)

        for i in range(self.input_dim):
            col = g[:, i]
            freq = (i + 1) / self.input_dim
            transformed[:, i] = (
                np.sin(col * freq)
                + 0.5 * np.cos(col * (1.0 - freq))
                + 0.15 * np.sign(col)
                + 0.1 * np.power(col, 2)
            )

        # Inject structured cross-feature dependencies.
        for i in range(0, self.input_dim, 4):
            end = min(i + 4, self.input_dim)
            block = transformed[:, i:end]
            transformed[:, i:end] = block + 0.2 * np.mean(block, axis=1, keepdims=True)

        # Normalize each feature.
        transformed -= np.mean(transformed, axis=0, keepdims=True)
        transformed /= np.std(transformed, axis=0, keepdims=True) + 1e-6
        return transformed

    def _teacher_logits(self, x: np.ndarray) -> np.ndarray:
        w1 = self.rng.normal(0, 0.8, size=(self.input_dim, self.input_dim)).astype(np.float32)
        w2 = self.rng.normal(0, 0.6, size=(self.input_dim, self.classes)).astype(np.float32)

        h = np.tanh(x @ w1)
        h = h + 0.3 * np.sin(h)
        logits = h @ w2

        # Apply a synthetic architecture-prior bias.
        class_bias = np.linspace(-0.4, 0.4, self.classes, dtype=np.float32)
        logits += class_bias[None, :]
        return logits

    def build(self, train_samples: int, val_samples: int) -> Dataset:
        x_train = self._latent_kernel(train_samples)
        x_val = self._latent_kernel(val_samples)

        logits_train = self._teacher_logits(x_train)
        logits_val = self._teacher_logits(x_val)

        y_train = np.argmax(logits_train + self.rng.normal(scale=0.6, size=logits_train.shape), axis=1)
        y_val = np.argmax(logits_val + self.rng.normal(scale=0.6, size=logits_val.shape), axis=1)

        return Dataset(
            x_train=x_train.astype(np.float32),
            y_train=y_train.astype(np.int64),
            x_val=x_val.astype(np.float32),
            y_val=y_val.astype(np.int64),
        )


def iterate_minibatches(
    x: np.ndarray,
    y: np.ndarray,
    batch_size: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    idx = np.arange(x.shape[0])
    rng.shuffle(idx)
    for start in range(0, x.shape[0], batch_size):
        batch_idx = idx[start : start + batch_size]
        yield x[batch_idx], y[batch_idx]
