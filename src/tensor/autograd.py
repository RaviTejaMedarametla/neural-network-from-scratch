from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class Context:
    saved_tensors: tuple[np.ndarray, ...] = ()

    def save_for_backward(self, *arrays: np.ndarray) -> None:
        self.saved_tensors = arrays


class Function:
    @staticmethod
    def forward(ctx: Context, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def backward(ctx: Context, grad_output):
        raise NotImplementedError


class Linear(Function):
    @staticmethod
    def forward(ctx: Context, x: np.ndarray, w: np.ndarray, b: np.ndarray | None = None) -> np.ndarray:
        ctx.save_for_backward(x, w)
        out = x @ w
        if b is not None:
            out = out + b
        return out

    @staticmethod
    def backward(ctx: Context, grad_output: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        x, w = ctx.saved_tensors
        return grad_output @ w.T, x.T @ grad_output
