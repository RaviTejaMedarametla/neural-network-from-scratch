from __future__ import annotations
import numpy as np

class Adam:
    def __init__(self, params: list[dict], lr: float = 1e-3, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8) -> None:
        self.params = params
        self.lr = lr
        self.b1 = beta1
        self.b2 = beta2
        self.eps = eps
        self.t = 0
        self.m = [np.zeros_like(p["param"]) for p in params]
        self.v = [np.zeros_like(p["param"]) for p in params]

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.params):
            g = p["grad"]
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * (g * g)
            mh = self.m[i] / (1 - self.b1 ** self.t)
            vh = self.v[i] / (1 - self.b2 ** self.t)
            p["param"] -= self.lr * mh / (np.sqrt(vh) + self.eps)

    def zero_grad(self) -> None:
        for p in self.params:
            p["grad"].fill(0.0)
