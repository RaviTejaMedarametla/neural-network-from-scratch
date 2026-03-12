from __future__ import annotations

import numpy as np


def sparsity_ratio(tensor: np.ndarray) -> float:
    """Return ratio of zero elements."""
    return float(np.sum(tensor == 0) / max(tensor.size, 1))


def simulate_sparse_matmul(weights: np.ndarray, x: np.ndarray) -> dict[str, float]:
    """Estimate sparse matmul speedup by non-zero MAC reduction."""
    nnz = int(np.sum(weights != 0))
    total = int(weights.size)
    dense_macs = x.shape[0] * total
    sparse_macs = x.shape[0] * nnz
    speedup = dense_macs / max(sparse_macs, 1)
    return {"dense_macs": float(dense_macs), "sparse_macs": float(sparse_macs), "speedup": float(speedup)}
