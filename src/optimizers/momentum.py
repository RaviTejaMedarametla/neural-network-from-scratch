from __future__ import annotations
import numpy as np

class MomentumSGD:
    def __init__(self, params: list[dict], lr: float = 1e-2, momentum: float = 0.9) -> None:
        self.params = params
        self.lr = lr
        self.momentum = momentum
        self.v = [np.zeros_like(p["param"]) for p in params]

    def step(self) -> None:
        for i, p in enumerate(self.params):
            self.v[i] = self.momentum * self.v[i] - self.lr * p["grad"]
            p["param"] += self.v[i]

    def zero_grad(self) -> None:
        for p in self.params:
            p["grad"].fill(0.0)
