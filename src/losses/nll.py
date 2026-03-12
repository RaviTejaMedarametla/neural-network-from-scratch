from __future__ import annotations
import numpy as np

class NLLLoss:
    def forward(self, log_probs: np.ndarray, target: np.ndarray) -> tuple[float, np.ndarray]:
        n = log_probs.shape[0]
        loss = -np.mean(log_probs[np.arange(n), target])
        grad = np.zeros_like(log_probs)
        grad[np.arange(n), target] = -1.0 / n
        return float(loss), grad
