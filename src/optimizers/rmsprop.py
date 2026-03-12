from __future__ import annotations
import numpy as np

class RMSprop:
    def __init__(self, params: list[dict], lr: float = 1e-3, alpha: float = 0.99, eps: float = 1e-8) -> None:
        self.params = params
        self.lr = lr
        self.alpha = alpha
        self.eps = eps
        self.v = [np.zeros_like(p["param"]) for p in params]

    def step(self) -> None:
        for i, p in enumerate(self.params):
            g = p["grad"]
            self.v[i] = self.alpha * self.v[i] + (1 - self.alpha) * (g * g)
            p["param"] -= self.lr * g / (np.sqrt(self.v[i]) + self.eps)

    def zero_grad(self) -> None:
        for p in self.params:
            p["grad"].fill(0.0)
