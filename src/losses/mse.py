from __future__ import annotations
import numpy as np

class MSELoss:
    def forward(self, pred: np.ndarray, target: np.ndarray) -> tuple[float, np.ndarray]:
        diff = pred - target
        loss = float(np.mean(diff**2))
        grad = 2.0 * diff / diff.size
        return loss, grad
