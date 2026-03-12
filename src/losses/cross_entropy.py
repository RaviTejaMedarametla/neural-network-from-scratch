from __future__ import annotations
import numpy as np

class CrossEntropyLoss:
    def forward(self, logits: np.ndarray, target: np.ndarray) -> tuple[float, np.ndarray]:
        shifted = logits - logits.max(axis=1, keepdims=True)
        ex = np.exp(shifted)
        probs = ex / ex.sum(axis=1, keepdims=True)
        n = logits.shape[0]
        loss = -np.mean(np.log(probs[np.arange(n), target] + 1e-9))
        grad = probs
        grad[np.arange(n), target] -= 1.0
        grad /= n
        return float(loss), grad
