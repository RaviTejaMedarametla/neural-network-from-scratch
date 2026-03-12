from __future__ import annotations
from .tensor import Tensor

def add(a: Tensor, b: Tensor) -> Tensor:
    return a + b

def mul(a: Tensor, b: Tensor) -> Tensor:
    return a * b

def matmul(a: Tensor, b: Tensor) -> Tensor:
    return a @ b
