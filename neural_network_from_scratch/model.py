from __future__ import annotations

import numpy as np


class SimpleMLP:
    """Tiny 1-hidden-layer MLP for binary classification."""

    def __init__(self, n_features: int, n_hidden: int = 16, seed: int = 42, lr: float = 0.1):
        if n_features < 1:
            raise ValueError("n_features must be >= 1")
        if n_hidden < 1:
            raise ValueError("n_hidden must be >= 1")
        if lr <= 0:
            raise ValueError("lr must be > 0")

        self.n_features = int(n_features)
        self.n_hidden = int(n_hidden)
        self.lr = float(lr)
        self.rng = np.random.default_rng(int(seed))

        self.w1 = self.rng.normal(0, 0.1, size=(self.n_features, self.n_hidden))
        self.b1 = np.zeros((1, self.n_hidden))
        self.w2 = self.rng.normal(0, 0.1, size=(self.n_hidden, 1))
        self.b2 = np.zeros((1, 1))

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-x))

    def forward(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=np.float64)
        if x.ndim != 2 or x.shape[1] != self.n_features:
            raise ValueError("x must be 2D with shape (n_samples, n_features)")
        h = np.tanh(x @ self.w1 + self.b1)
        out = self._sigmoid(h @ self.w2 + self.b2)
        return out

    def predict(self, x: np.ndarray) -> np.ndarray:
        return (self.forward(x).ravel() >= 0.5).astype(np.int64)

    def fit(self, x: np.ndarray, y: np.ndarray, epochs: int = 100) -> None:
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1, 1)
        if x.shape[0] != y.shape[0]:
            raise ValueError("x and y must have same number of rows")

        for _ in range(int(epochs)):
            h_pre = x @ self.w1 + self.b1
            h = np.tanh(h_pre)
            out_pre = h @ self.w2 + self.b2
            out = self._sigmoid(out_pre)

            d_out = (out - y) / y.shape[0]
            dw2 = h.T @ d_out
            db2 = np.sum(d_out, axis=0, keepdims=True)

            d_h = (d_out @ self.w2.T) * (1 - np.tanh(h_pre) ** 2)
            dw1 = x.T @ d_h
            db1 = np.sum(d_h, axis=0, keepdims=True)

            self.w2 -= self.lr * dw2
            self.b2 -= self.lr * db2
            self.w1 -= self.lr * dw1
            self.b1 -= self.lr * db1


NeuralNetwork = SimpleMLP
