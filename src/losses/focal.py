from __future__ import annotations

import numpy as np


class FocalLoss:
    """Focal loss for class-imbalanced classification."""

    def __init__(self, gamma: float = 2.0, alpha: np.ndarray | None = None) -> None:
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, pred: np.ndarray, target: np.ndarray) -> float:
        probs = np.exp(pred - np.max(pred, axis=1, keepdims=True))
        probs /= np.sum(probs, axis=1, keepdims=True)
        p = probs[np.arange(pred.shape[0]), target]
        weight = (1.0 - p) ** self.gamma
        if self.alpha is not None:
            weight *= self.alpha[target]
        return float(np.mean(-weight * np.log(p + 1e-8)))
