from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .math_ops import (
    dropout_backward,
    dropout_forward,
    gelu,
    gelu_backward,
    layer_norm_backward,
    layer_norm_forward,
    relu,
    relu_backward,
    tanh,
    tanh_backward,
)


@dataclass
class Parameter:
    data: np.ndarray
    grad: np.ndarray
    name: str


class Dense:
    def __init__(self, in_dim: int, out_dim: int, init: str, name: str, rng: np.random.Generator) -> None:
        self.name = name
        if init == "xavier":
            scale = np.sqrt(2.0 / (in_dim + out_dim))
        elif init == "he":
            scale = np.sqrt(2.0 / in_dim)
        else:
            scale = 0.02
        self.w = Parameter(
            data=(rng.normal(size=(in_dim, out_dim)).astype(np.float32) * scale),
            grad=np.zeros((in_dim, out_dim), dtype=np.float32),
            name=f"{name}.weight",
        )
        self.b = Parameter(
            data=np.zeros((1, out_dim), dtype=np.float32),
            grad=np.zeros((1, out_dim), dtype=np.float32),
            name=f"{name}.bias",
        )
        self._cache_x: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self._cache_x = x
        return x @ self.w.data + self.b.data

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        if self._cache_x is None:
            raise RuntimeError("Dense backward called before forward")
        x = self._cache_x
        self.w.grad += x.T @ grad_output
        self.b.grad += np.sum(grad_output, axis=0, keepdims=True)
        grad_input = grad_output @ self.w.data.T
        self._cache_x = None
        return grad_input

    def parameters(self) -> list[Parameter]:
        return [self.w, self.b]


class Activation:
    def __init__(self, kind: str):
        self.kind = kind
        self._cache_x: np.ndarray | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self._cache_x = x
        if self.kind == "relu":
            return relu(x)
        if self.kind == "gelu":
            return gelu(x)
        if self.kind == "tanh":
            return tanh(x)
        raise ValueError(f"Unknown activation: {self.kind}")

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        if self._cache_x is None:
            raise RuntimeError("Activation backward called before forward")
        x = self._cache_x
        self._cache_x = None
        if self.kind == "relu":
            return relu_backward(x, grad_output)
        if self.kind == "gelu":
            return gelu_backward(x, grad_output)
        if self.kind == "tanh":
            return tanh_backward(x, grad_output)
        raise ValueError(f"Unknown activation: {self.kind}")


class LayerNorm:
    def __init__(self, dim: int, name: str):
        self.gamma = Parameter(np.ones((1, dim), dtype=np.float32), np.zeros((1, dim), dtype=np.float32), f"{name}.gamma")
        self.beta = Parameter(np.zeros((1, dim), dtype=np.float32), np.zeros((1, dim), dtype=np.float32), f"{name}.beta")
        self._cache: dict[str, np.ndarray] | None = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        x_hat, cache = layer_norm_forward(x)
        self._cache = cache
        return self.gamma.data * x_hat + self.beta.data

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        if self._cache is None:
            raise RuntimeError("LayerNorm backward called before forward")
        x_hat = self._cache["x_hat"]
        self.gamma.grad += np.sum(grad_output * x_hat, axis=0, keepdims=True)
        self.beta.grad += np.sum(grad_output, axis=0, keepdims=True)
        grad_xhat = grad_output * self.gamma.data
        grad_input = layer_norm_backward(grad_xhat, self._cache)
        self._cache = None
        return grad_input

    def parameters(self) -> list[Parameter]:
        return [self.gamma, self.beta]


class Dropout:
    def __init__(self, p: float, rng: np.random.Generator):
        self.p = p
        self.rng = rng
        self._mask: np.ndarray | None = None

    def forward(self, x: np.ndarray, training: bool) -> np.ndarray:
        y, self._mask = dropout_forward(x, self.p, training, self.rng)
        return y

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        out = dropout_backward(grad_output, self._mask)
        self._mask = None
        return out


class MLPModel:
    """Simple MLP with explicit forward/backward passes for educational and profiling use."""

    def __init__(
        self,
        input_dim: int,
        hidden_dims: list[int],
        output_dim: int,
        activation: str,
        init: str,
        dropout: float,
        layer_norm: bool,
        seed: int,
    ) -> None:
        rng = np.random.default_rng(seed)
        dims = [input_dim, *hidden_dims, output_dim]

        self.layers: list[Dense] = []
        self.activations: list[Activation] = []
        self.norms: list[LayerNorm | None] = []
        self.dropouts: list[Dropout | None] = []

        for i in range(len(dims) - 1):
            self.layers.append(Dense(dims[i], dims[i + 1], init=init, name=f"dense_{i}", rng=rng))
            is_last = i == len(dims) - 2
            if not is_last:
                self.activations.append(Activation(activation))
                self.norms.append(LayerNorm(dims[i + 1], name=f"ln_{i}") if layer_norm else None)
                self.dropouts.append(Dropout(dropout, rng=rng) if dropout > 0 else None)

    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        h = x
        for i, dense in enumerate(self.layers):
            h = dense.forward(h)
            is_last = i == len(self.layers) - 1
            if is_last:
                continue
            norm = self.norms[i]
            if norm is not None:
                h = norm.forward(h)
            h = self.activations[i].forward(h)
            drop = self.dropouts[i]
            if drop is not None:
                h = drop.forward(h, training=training)
        return h

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        grad = grad_output
        for i in reversed(range(len(self.layers))):
            is_last = i == len(self.layers) - 1
            if not is_last:
                drop = self.dropouts[i]
                if drop is not None:
                    grad = drop.backward(grad)
                grad = self.activations[i].backward(grad)
                norm = self.norms[i]
                if norm is not None:
                    grad = norm.backward(grad)
            grad = self.layers[i].backward(grad)
        return grad

    def zero_grad(self) -> None:
        for p in self.parameters():
            p.grad.fill(0.0)

    def parameters(self) -> list[Parameter]:
        params: list[Parameter] = []
        for layer in self.layers:
            params.extend(layer.parameters())
        for n in self.norms:
            if n is not None:
                params.extend(n.parameters())
        return params
