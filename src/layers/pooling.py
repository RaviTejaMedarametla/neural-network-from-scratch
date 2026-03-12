from __future__ import annotations

import numpy as np

from .base import Layer


class MaxPool2D(Layer):
    """2D max pooling layer."""

    def __init__(self, pool_size: int = 2, stride: int | None = None) -> None:
        super().__init__()
        self.pool_size = pool_size
        self.stride = stride or pool_size
        self.cache: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        n, c, h, w = x.shape
        out_h = (h - self.pool_size) // self.stride + 1
        out_w = (w - self.pool_size) // self.stride + 1
        out = np.zeros((n, c, out_h, out_w), dtype=x.dtype)
        self.cache = x
        for i in range(out_h):
            for j in range(out_w):
                hs, ws = i * self.stride, j * self.stride
                window = x[:, :, hs : hs + self.pool_size, ws : ws + self.pool_size]
                out[:, :, i, j] = np.max(window.reshape(n, c, -1), axis=2)
        return out

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        if self.cache is None:
            raise RuntimeError("forward must run before backward")
        x = self.cache
        grad_input = np.zeros_like(x)
        n, c, _, _ = x.shape
        out_h, out_w = grad_output.shape[2], grad_output.shape[3]
        for i in range(out_h):
            for j in range(out_w):
                hs, ws = i * self.stride, j * self.stride
                window = x[:, :, hs : hs + self.pool_size, ws : ws + self.pool_size]
                max_vals = np.max(window.reshape(n, c, -1), axis=2)[:, :, None, None]
                mask = window == max_vals
                grad_input[:, :, hs : hs + self.pool_size, ws : ws + self.pool_size] += (
                    mask * grad_output[:, :, i : i + 1, j : j + 1]
                )
        return grad_input


class AvgPool2D(Layer):
    """2D average pooling layer."""

    def __init__(self, pool_size: int = 2, stride: int | None = None) -> None:
        super().__init__()
        self.pool_size = pool_size
        self.stride = stride or pool_size
        self.input_shape: tuple[int, ...] | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.input_shape = x.shape
        n, c, h, w = x.shape
        out_h = (h - self.pool_size) // self.stride + 1
        out_w = (w - self.pool_size) // self.stride + 1
        out = np.zeros((n, c, out_h, out_w), dtype=x.dtype)
        for i in range(out_h):
            for j in range(out_w):
                hs, ws = i * self.stride, j * self.stride
                window = x[:, :, hs : hs + self.pool_size, ws : ws + self.pool_size]
                out[:, :, i, j] = np.mean(window, axis=(2, 3))
        return out

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        if self.input_shape is None:
            raise RuntimeError("forward must run before backward")
        n, c, h, w = self.input_shape
        grad_input = np.zeros((n, c, h, w), dtype=grad_output.dtype)
        scale = 1.0 / (self.pool_size * self.pool_size)
        out_h, out_w = grad_output.shape[2], grad_output.shape[3]
        for i in range(out_h):
            for j in range(out_w):
                hs, ws = i * self.stride, j * self.stride
                grad_input[:, :, hs : hs + self.pool_size, ws : ws + self.pool_size] += (
                    grad_output[:, :, i : i + 1, j : j + 1] * scale
                )
        return grad_input
