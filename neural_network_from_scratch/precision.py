"""Precision and quantization utilities for scratch neural networks."""

from __future__ import annotations

import numpy as np


class PrecisionMixin:
    """Utilities for inference in reduced precision modes."""

    infer_precision: str
    int8_clip_value: int

    def _quantize_to_int8(self, x: np.ndarray) -> tuple[np.ndarray, float]:
        max_abs = np.max(np.abs(x))
        if max_abs == 0:
            return np.zeros_like(x, dtype=np.int8), 1.0
        scale = max_abs / float(self.int8_clip_value)
        q = np.clip(np.round(x / scale), -self.int8_clip_value, self.int8_clip_value).astype(np.int8)
        return q, scale

    @staticmethod
    def _dequantize_from_int8(q: np.ndarray, scale: float) -> np.ndarray:
        return q.astype(np.float32) * np.float32(scale)
