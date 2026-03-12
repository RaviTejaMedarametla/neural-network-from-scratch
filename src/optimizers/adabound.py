from __future__ import annotations

import numpy as np


class AdaBound:
    """AdaBound optimizer with dynamic bounds on adaptive learning rates."""

    def __init__(
        self,
        params: list[dict],
        lr: float = 1e-3,
        final_lr: float = 0.1,
        beta1: float = 0.9,
        beta2: float = 0.999,
        gamma: float = 1e-3,
        eps: float = 1e-8,
    ) -> None:
        self.params = params
        self.lr = lr
        self.final_lr = final_lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.gamma = gamma
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

            step_size = self.lr / (np.sqrt(v_hat) + self.eps)
            lower = self.final_lr * (1 - 1 / (self.gamma * self.t + 1))
            upper = self.final_lr * (1 + 1 / (self.gamma * self.t))
            step_size = np.clip(step_size, lower, upper)
            p["param"] -= step_size * m_hat

    def zero_grad(self) -> None:
        for p in self.params:
            p["grad"].fill(0.0)
