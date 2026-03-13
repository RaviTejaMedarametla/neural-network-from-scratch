from __future__ import annotations

import numpy as np

from .base import Layer


class Conv2D(Layer):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, stride: int = 1, padding: int = 0, bias: bool = True, dtype: str = "float32") -> None:
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.w = np.random.randn(out_channels, in_channels, kernel_size, kernel_size).astype(np.float32) * 0.02
        self.b = np.zeros((out_channels,), dtype=np.float32) if bias else None
        self.dw = np.zeros_like(self.w)
        self.db = np.zeros_like(self.b) if self.b is not None else None
        self.x: np.ndarray | None = None
        self.dtype = dtype

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.x = x
        n, _, h, w = x.shape
        k = self.kernel_size
        oh = (h + 2 * self.padding - k) // self.stride + 1
        ow = (w + 2 * self.padding - k) // self.stride + 1
        out = np.zeros((n, self.out_channels, oh, ow), dtype=np.float32)
        xp = np.pad(x, ((0, 0), (0, 0), (self.padding, self.padding), (self.padding, self.padding)))
        for i in range(oh):
            for j in range(ow):
                hs = i * self.stride
                ws = j * self.stride
                region = xp[:, :, hs : hs + k, ws : ws + k]
                out[:, :, i, j] = np.tensordot(region, self.w, axes=((1, 2, 3), (1, 2, 3)))
        if self.b is not None:
            out += self.b[None, :, None, None]
        return out

    def backward(self, grad: np.ndarray) -> np.ndarray:
        assert self.x is not None
        x = self.x
        n, _, h, w = x.shape
        k = self.kernel_size
        oh = grad.shape[2]
        ow = grad.shape[3]

        xp = np.pad(x, ((0, 0), (0, 0), (self.padding, self.padding), (self.padding, self.padding)))
        dxp = np.zeros_like(xp)
        self.dw.fill(0.0)

        if self.db is not None:
            self.db = grad.sum(axis=(0, 2, 3))

        for i in range(oh):
            for j in range(ow):
                hs = i * self.stride
                ws = j * self.stride
                region = xp[:, :, hs : hs + k, ws : ws + k]

                self.dw += np.tensordot(grad[:, :, i, j], region, axes=((0,), (0,)))
                dxp[:, :, hs : hs + k, ws : ws + k] += np.tensordot(
                    grad[:, :, i, j],
                    self.w,
                    axes=((1,), (0,)),
                )

        if self.padding > 0:
            return dxp[:, :, self.padding : self.padding + h, self.padding : self.padding + w]
        return dxp

    def parameters(self) -> list[dict[str, np.ndarray]]:
        p = [{"param": self.w, "grad": self.dw}]
        if self.b is not None and self.db is not None:
            p.append({"param": self.b, "grad": self.db})
        return p

    def flops(self, input_shape: tuple[int, ...]) -> int:
        n, _, h, w = input_shape
        k = self.kernel_size
        oh = (h + 2 * self.padding - k) // self.stride + 1
        ow = (w + 2 * self.padding - k) // self.stride + 1
        return int(n * oh * ow * self.out_channels * self.in_channels * k * k * 2)

    def memory_footprint(self) -> int:
        total = self.w.nbytes + self.dw.nbytes
        if self.b is not None and self.db is not None:
            total += self.b.nbytes + self.db.nbytes
        return int(total)
