from __future__ import annotations

import numpy as np

from .attention import SelfAttention
from .base import Layer
from .dense import Dense


class TransformerBlock(Layer):
    """Transformer encoder block with residuals and layernorm."""

    def __init__(self, embed_dim: int, num_heads: int, ff_hidden: int) -> None:
        super().__init__()
        self.attn = SelfAttention(embed_dim, num_heads)
        self.ff1 = Dense(embed_dim, ff_hidden)
        self.ff2 = Dense(ff_hidden, embed_dim)
        self.eps = 1e-5
        self.cache: dict[str, np.ndarray] = {}

    def _layernorm(self, x: np.ndarray) -> tuple[np.ndarray, tuple[np.ndarray, np.ndarray]]:
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        out = (x - mean) / np.sqrt(var + self.eps)
        return out, (mean, var)

    def forward(self, x: np.ndarray) -> np.ndarray:
        attn_out = self.attn.forward(x)
        h1, ln1 = self._layernorm(x + attn_out)

        ff = np.maximum(0.0, self.ff1.forward(h1.reshape(-1, h1.shape[-1])))
        ff = self.ff2.forward(ff).reshape(h1.shape)
        out, ln2 = self._layernorm(h1 + ff)

        self.cache = {"x": x, "h1": h1, "ln1_mean": ln1[0], "ln1_var": ln1[1], "ln2_mean": ln2[0], "ln2_var": ln2[1]}
        return out

    def backward(self, grad: np.ndarray) -> np.ndarray:
        # Approximate backward through residual stack.
        gh1 = grad
        gff = grad
        gff2 = self.ff2.backward(gff.reshape(-1, gff.shape[-1]))
        gff1 = self.ff1.backward(gff2)
        gff1 = gff1.reshape(self.cache["h1"].shape)
        gattn = self.attn.backward(gh1)
        return gattn + gff1 + grad

    def parameters(self) -> list[dict[str, np.ndarray]]:
        params: list[dict[str, np.ndarray]] = []
        params.extend(self.attn.parameters())
        params.extend(self.ff1.parameters())
        params.extend(self.ff2.parameters())
        return params
