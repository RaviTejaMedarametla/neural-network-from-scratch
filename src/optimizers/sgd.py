from __future__ import annotations

class SGD:
    def __init__(self, params: list[dict], lr: float = 1e-2, weight_decay: float = 0.0) -> None:
        self.params = params
        self.lr = lr
        self.weight_decay = weight_decay

    def step(self) -> None:
        for p in self.params:
            p["param"] -= self.lr * (p["grad"] + self.weight_decay * p["param"])

    def zero_grad(self) -> None:
        for p in self.params:
            p["grad"].fill(0.0)
