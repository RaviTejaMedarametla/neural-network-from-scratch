from __future__ import annotations

import numpy as np
from src.layers.base import Layer


class Sequential:
    """Simple sequential container for layers."""

    def __init__(self, layers: list[Layer] | None = None) -> None:
        self.layers: list[Layer] = layers or []

    def add(self, layer: Layer) -> None:
        """Append a layer to the model."""
        self.layers.append(layer)

    def forward(self, x: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, grad: np.ndarray) -> np.ndarray:
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
        return grad

    def parameters(self) -> list[dict[str, np.ndarray]]:
        params: list[dict[str, np.ndarray]] = []
        for layer in self.layers:
            params.extend(layer.parameters())
        return params

    def named_parameters(self) -> list[tuple[str, dict[str, np.ndarray]]]:
        named: list[tuple[str, dict[str, np.ndarray]]] = []
        for i, layer in enumerate(self.layers):
            for j, p in enumerate(layer.parameters()):
                named.append((f"layer{i}.param{j}", p))
        return named

    def zero_grad(self) -> None:
        for p in self.parameters():
            p["grad"].fill(0.0)

    def train(self) -> None:
        for layer in self.layers:
            layer.train()

    def eval(self) -> None:
        for layer in self.layers:
            layer.eval()

    def to(self, device: str) -> "Sequential":
        for layer in self.layers:
            layer.to(device)
        return self

    def quantize(self, bits: int = 8) -> None:
        for layer in self.layers:
            layer.quantize(bits)

    def flops(self, input_shape: tuple[int, ...]) -> int:
        total = 0
        for layer in self.layers:
            total += layer.flops(input_shape)
        return total

    def memory_footprint(self) -> int:
        return sum(layer.memory_footprint() for layer in self.layers)

    def summary(self) -> str:
        lines = ["Model Summary:"]
        for i, layer in enumerate(self.layers):
            lines.append(f"[{i}] {layer.__class__.__name__} mem={layer.memory_footprint()}B")
        lines.append(f"Total memory: {self.memory_footprint()}B")
        return "\n".join(lines)
