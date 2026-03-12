from __future__ import annotations

import numpy as np

from .base import Layer


class Embedding(Layer):
    """Embedding layer for integer token indices."""

    def __init__(self, num_embeddings: int, embedding_dim: int) -> None:
        super().__init__()
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self.weights = np.random.randn(num_embeddings, embedding_dim).astype(np.float32) * 0.01
        self.grad_weights = np.zeros_like(self.weights)
        self.cache: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.cache = x.astype(np.int64)
        return self.weights[self.cache]

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        if self.cache is None:
            raise RuntimeError("forward must run before backward")
        self.grad_weights.fill(0.0)
        np.add.at(self.grad_weights, self.cache, grad_output)
        return np.zeros_like(self.cache, dtype=np.float32)

    def parameters(self) -> list[dict[str, np.ndarray]]:
        return [{"param": self.weights, "grad": self.grad_weights}]
