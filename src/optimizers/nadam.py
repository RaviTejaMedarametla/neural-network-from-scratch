from __future__ import annotations

import numpy as np


class Nadam:
    """Nesterov-accelerated Adam."""

    def __init__(self, params: list[dict], lr: float = 1e-3, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8) -> None:
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = [np.zeros_like(p["param"]) for p in params]
        self.v = [np.zeros_like(p["param"]) for p in params]

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.params):
            g = p["grad"]
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (g * g)
            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)
            m_nesterov = self.beta1 * m_hat + (1 - self.beta1) * g / (1 - self.beta1**self.t)
            p["param"] -= self.lr * m_nesterov / (np.sqrt(v_hat) + self.eps)

    def zero_grad(self) -> None:
        for p in self.params:
            p["grad"].fill(0.0)
