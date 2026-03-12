from __future__ import annotations

import numpy as np


class KLDivLoss:
    """KL divergence for log-probabilities."""

    def forward(self, pred_log: np.ndarray, target_log: np.ndarray) -> float:
        return float(np.mean(np.sum(np.exp(target_log) * (target_log - pred_log), axis=1)))
