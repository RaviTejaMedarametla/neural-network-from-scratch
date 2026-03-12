from __future__ import annotations

import numpy as np

from .layers import Parameter


class SGD:
    def __init__(self, params: list[Parameter], lr: float, weight_decay: float = 0.0):
        self.params = params
        self.lr = lr
        self.weight_decay = weight_decay

    def step(self) -> None:
        for p in self.params:
            grad = p.grad + self.weight_decay * p.data
            p.data -= self.lr * grad


class Adam:
    def __init__(
        self,
        params: list[Parameter],
        lr: float,
        weight_decay: float = 0.0,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
    ):
        self.params = params
        self.lr = lr
        self.weight_decay = weight_decay
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = [np.zeros_like(p.data) for p in self.params]
        self.v = [np.zeros_like(p.data) for p in self.params]

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.params):
            grad = p.grad + self.weight_decay * p.data
            self.m[i] = self.beta1 * self.m[i] + (1.0 - self.beta1) * grad
            self.v[i] = self.beta2 * self.v[i] + (1.0 - self.beta2) * (grad * grad)

            m_hat = self.m[i] / (1.0 - self.beta1**self.t)
            v_hat = self.v[i] / (1.0 - self.beta2**self.t)
            p.data -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


def make_optimizer(name: str, params: list[Parameter], lr: float, weight_decay: float):
    if name == "sgd":
        return SGD(params=params, lr=lr, weight_decay=weight_decay)
    if name == "adam":
        return Adam(params=params, lr=lr, weight_decay=weight_decay)
    raise ValueError(f"Unknown optimizer: {name}")
