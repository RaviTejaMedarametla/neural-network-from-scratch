from __future__ import annotations
import numpy as np


class Quantizer:
    def __init__(self, bits: int = 8, scheme: str = "symmetric") -> None:
        self.bits = bits
        self.scheme = scheme

    def quantize(self, tensor: np.ndarray, bits: int | None = None, scheme: str | None = None) -> tuple[np.ndarray, float]:
        bits = bits or self.bits
        scheme = scheme or self.scheme
        if bits == 1:
            q = np.where(tensor >= 0, 1, -1).astype(np.int8)
            return q, 1.0
        qmax = 2 ** (bits - 1) - 1
        if scheme == "symmetric":
            scale = np.max(np.abs(tensor)) / max(qmax, 1)
            scale = max(scale, 1e-9)
            q = np.round(tensor / scale).clip(-qmax, qmax).astype(np.int32)
            return q, float(scale)
        mn, mx = tensor.min(), tensor.max()
        scale = (mx - mn) / max((2**bits - 1), 1)
        zp = int(round(-mn / max(scale, 1e-9)))
        q = np.round(tensor / max(scale, 1e-9) + zp).clip(0, 2**bits - 1).astype(np.int32)
        return q, float(scale)

    def dequantize(self, q: np.ndarray, scale: float) -> np.ndarray:
        return (q.astype(np.float32) * scale).astype(np.float32)


def quantization_error(original: np.ndarray, restored: np.ndarray) -> float:
    return float(np.mean((original - restored) ** 2))
