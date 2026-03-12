from __future__ import annotations
import numpy as np


def xavier(shape: tuple[int, ...]) -> np.ndarray:
    fan_in, fan_out = shape[0], shape[1]
    limit = np.sqrt(6 / (fan_in + fan_out))
    return np.random.uniform(-limit, limit, size=shape).astype(np.float32)


def he(shape: tuple[int, ...]) -> np.ndarray:
    fan_in = shape[0]
    return (np.random.randn(*shape) * np.sqrt(2 / fan_in)).astype(np.float32)


def normal(shape: tuple[int, ...], std: float = 0.02) -> np.ndarray:
    return (np.random.randn(*shape) * std).astype(np.float32)


def uniform(shape: tuple[int, ...], low: float = -0.1, high: float = 0.1) -> np.ndarray:
    return np.random.uniform(low, high, size=shape).astype(np.float32)
