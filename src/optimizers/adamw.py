from __future__ import annotations

import numpy as np


class AdamW:
    """AdamW optimizer with decoupled weight decay."""

    def __init__(
        self,
        params: list[dict],
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 1e-2,
    ) -> None:
        self.params = params
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.t = 0
        self.m = [np.zeros_like(p["param"]) for p in params]
        self.v = [np.zeros_like(p["param"]) for p in params]

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.params):
            g = p["grad"]
            p["param"] -= self.lr * self.weight_decay * p["param"]
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (g * g)
            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)
            p["param"] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

    def zero_grad(self) -> None:
        for p in self.params:
            p["grad"].fill(0.0)
