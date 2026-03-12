from __future__ import annotations
import numpy as np
from .base import Layer


class Dense(Layer):
    def __init__(self, in_features: int, out_features: int, bias: bool = True, dtype: str = "float32") -> None:
        super().__init__()
        scale = np.sqrt(2.0 / in_features)
        self.w = np.random.randn(in_features, out_features).astype(np.float32) * scale
        self.b = np.zeros((1, out_features), dtype=np.float32) if bias else None
        self.dw = np.zeros_like(self.w)
        self.db = np.zeros_like(self.b) if self.b is not None else None
        self.x: np.ndarray | None = None
        self.dtype = dtype

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.x = x
        y = x @ self.w
        if self.b is not None:
            y = y + self.b
        return y

    def backward(self, grad: np.ndarray) -> np.ndarray:
        assert self.x is not None
        self.dw = self.x.T @ grad
        if self.b is not None and self.db is not None:
            self.db = grad.sum(axis=0, keepdims=True)
        return grad @ self.w.T

    def parameters(self) -> list[dict[str, np.ndarray]]:
        params = [{"param": self.w, "grad": self.dw}]
        if self.b is not None and self.db is not None:
            params.append({"param": self.b, "grad": self.db})
        return params

    def flops(self, input_shape: tuple[int, ...]) -> int:
        batch = input_shape[0]
        return int(batch * self.w.shape[0] * self.w.shape[1] * 2)

    def memory_footprint(self) -> int:
        total = self.w.nbytes + self.dw.nbytes
        if self.b is not None and self.db is not None:
            total += self.b.nbytes + self.db.nbytes
        return total

    def quantize(self, bits: int = 8) -> None:
        qmax = 2 ** (bits - 1) - 1
        scale = np.max(np.abs(self.w)) / max(qmax, 1)
        if scale == 0:
            return
        self.w = (np.round(self.w / scale).clip(-qmax, qmax) * scale).astype(np.float32)
