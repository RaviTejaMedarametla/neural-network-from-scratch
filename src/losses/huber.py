from __future__ import annotations

import numpy as np


class HuberLoss:
    """Huber loss for robust regression."""

    def __init__(self, delta: float = 1.0) -> None:
        self.delta = delta

    def forward(self, pred: np.ndarray, target: np.ndarray) -> float:
        diff = pred - target
        abs_diff = np.abs(diff)
        quadratic = np.minimum(abs_diff, self.delta)
        linear = abs_diff - quadratic
        loss = 0.5 * quadratic**2 + self.delta * linear
        return float(np.mean(loss))
