from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np


@dataclass
class TensorMetadata:
    dtype: str = "float32"
    device: str = "cpu"


class Tensor:
    """Autograd-capable tensor based on NumPy arrays."""

    def __init__(
        self,
        data: np.ndarray | list[float] | float,
        requires_grad: bool = False,
        dtype: str = "float32",
        device: str = "cpu",
    ) -> None:
        self.data = np.asarray(data, dtype=np.float32 if dtype in {"float32", "float16"} else np.float32)
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self.requires_grad = requires_grad
        self._backward: Callable[[], None] = lambda: None
        self._prev: set[Tensor] = set()
        self.meta = TensorMetadata(dtype=dtype, device=device)

    def __hash__(self) -> int:
        return id(self)

    @property
    def shape(self) -> tuple[int, ...]:
        return self.data.shape

    def zero_grad(self) -> None:
        if self.grad is not None:
            self.grad.fill(0.0)

    def to(self, device: str) -> "Tensor":
        self.meta.device = device
        return self

    def flops(self) -> int:
        return int(np.prod(self.shape))

    def memory_bytes(self) -> int:
        return int(self.data.nbytes + (0 if self.grad is None else self.grad.nbytes))

    def backward(self, grad: np.ndarray | None = None) -> None:
        if not self.requires_grad:
            return
        if grad is None:
            grad = np.ones_like(self.data)
        self.grad = grad if self.grad is None else self.grad + grad

        topo: list[Tensor] = []
        visited: set[Tensor] = set()

        def build(v: Tensor) -> None:
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build(child)
                topo.append(v)

        build(self)
        for node in reversed(topo):
            node._backward()

    def _op(self, other: "Tensor | float", forward, backward) -> "Tensor":
        o = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(forward(self.data, o.data), self.requires_grad or o.requires_grad)
        out._prev = {self, o}

        def _bw() -> None:
            if out.grad is None:
                return
            g1, g2 = backward(self.data, o.data, out.grad)
            if self.requires_grad:
                self.grad = g1 if self.grad is None else self.grad + g1
            if o.requires_grad:
                o.grad = g2 if o.grad is None else o.grad + g2

        out._backward = _bw
        return out

    def __add__(self, other: "Tensor | float") -> "Tensor":
        return self._op(other, lambda a, b: a + b, lambda a, b, g: (g, g))

    def __sub__(self, other: "Tensor | float") -> "Tensor":
        return self._op(other, lambda a, b: a - b, lambda a, b, g: (g, -g))

    def __mul__(self, other: "Tensor | float") -> "Tensor":
        return self._op(other, lambda a, b: a * b, lambda a, b, g: (g * b, g * a))

    def __truediv__(self, other: "Tensor | float") -> "Tensor":
        return self._op(other, lambda a, b: a / b, lambda a, b, g: (g / b, -g * a / (b * b)))

    def __neg__(self) -> "Tensor":
        out = Tensor(-self.data, self.requires_grad)
        out._prev = {self}

        def _bw() -> None:
            if self.requires_grad and out.grad is not None:
                self.grad = -out.grad if self.grad is None else self.grad - out.grad

        out._backward = _bw
        return out

    def __pow__(self, power: float) -> "Tensor":
        out = Tensor(self.data ** power, self.requires_grad)
        out._prev = {self}

        def _bw() -> None:
            if self.requires_grad and out.grad is not None:
                grad = power * (self.data ** (power - 1.0)) * out.grad
                self.grad = grad if self.grad is None else self.grad + grad

        out._backward = _bw
        return out

    def __matmul__(self, other: "Tensor") -> "Tensor":
        out = Tensor(self.data @ other.data, self.requires_grad or other.requires_grad)
        out._prev = {self, other}

        def _bw() -> None:
            if out.grad is None:
                return
            if self.requires_grad:
                grad = out.grad @ other.data.T
                self.grad = grad if self.grad is None else self.grad + grad
            if other.requires_grad:
                grad = self.data.T @ out.grad
                other.grad = grad if other.grad is None else other.grad + grad

        out._backward = _bw
        return out

    def sum(self, axis=None, keepdims=False) -> "Tensor":
        out = Tensor(self.data.sum(axis=axis, keepdims=keepdims), self.requires_grad)
        out._prev = {self}

        def _bw() -> None:
            if self.requires_grad and out.grad is not None:
                grad = np.broadcast_to(out.grad, self.data.shape)
                self.grad = grad if self.grad is None else self.grad + grad

        out._backward = _bw
        return out

    def mean(self, axis=None, keepdims=False) -> "Tensor":
        denom = self.data.size if axis is None else self.data.shape[axis]
        return self.sum(axis=axis, keepdims=keepdims) / float(denom)

    def reshape(self, *shape: int) -> "Tensor":
        out = Tensor(self.data.reshape(*shape), self.requires_grad)
        out._prev = {self}

        def _bw() -> None:
            if self.requires_grad and out.grad is not None:
                grad = out.grad.reshape(self.data.shape)
                self.grad = grad if self.grad is None else self.grad + grad

        out._backward = _bw
        return out

    def transpose(self, axes=None) -> "Tensor":
        out = Tensor(self.data.transpose(axes), self.requires_grad)
        out._prev = {self}

        def _bw() -> None:
            if self.requires_grad and out.grad is not None:
                grad = out.grad.transpose(axes)
                self.grad = grad if self.grad is None else self.grad + grad

        out._backward = _bw
        return out
