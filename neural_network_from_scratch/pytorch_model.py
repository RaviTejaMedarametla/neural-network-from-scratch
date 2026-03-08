"""PyTorch model equivalent to the scratch architecture."""

from __future__ import annotations

from typing import List

import numpy as np

from neural_network_from_scratch.data_utils import one_hot
from neural_network_from_scratch.reproducibility import set_global_seed

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:  # optional dependency
    torch = None
    nn = None
    F = None


def is_torch_available() -> bool:
    return torch is not None


class TorchMLP(nn.Module if nn is not None else object):
    def __init__(self, layer_sizes: List[int], activations: List[str]):
        if nn is None:
            raise RuntimeError("TorchMLP requires torch installed")
        super().__init__()
        if len(layer_sizes) < 2:
            raise ValueError("layer_sizes must include input and output")
        if len(activations) != len(layer_sizes) - 1:
            raise ValueError("activations length must match number of layers")

        self.activations = activations
        self.layers = nn.ModuleList(
            [nn.Linear(layer_sizes[i], layer_sizes[i + 1]) for i in range(len(layer_sizes) - 1)]
        )

    @staticmethod
    def _apply_activation(x, activation_name: str):
        name = activation_name.lower()
        if name == "relu":
            return F.relu(x)
        if name == "sigmoid":
            return torch.sigmoid(x)
        if name == "softmax":
            return F.softmax(x, dim=1)
        if name == "linear":
            return x
        raise ValueError(f"Unsupported activation: {activation_name}")

    def forward(self, x):
        out = x
        for layer, activation_name in zip(self.layers, self.activations):
            out = self._apply_activation(layer(out), activation_name)
        return out


class TorchNeuralNetwork:
    def __init__(self, layer_sizes, activations, seed=42):
        if torch is None:
            raise RuntimeError("PyTorch is not installed; cannot create TorchNeuralNetwork")

        self.layer_sizes = list(layer_sizes)
        self.activations = list(activations)
        self.seed = int(seed)
        self.device = torch.device("cpu")
        set_global_seed(self.seed)
        self.model = TorchMLP(self.layer_sizes, self.activations).to(self.device)

    def fit(self, X, y, epochs=10, alpha=0.1, batch_size=32, shuffle=True, seed=42):
        set_global_seed(seed)
        X_np = X.astype(np.float32)
        y_one_hot = one_hot(y, self.layer_sizes[-1])

        X_tensor = torch.from_numpy(X_np).to(self.device)
        y_tensor = torch.from_numpy(y_one_hot).to(self.device)

        optimizer = torch.optim.SGD(self.model.parameters(), lr=alpha)
        history = {"loss": [], "accuracy": []}

        n_samples = X_tensor.shape[0]
        idx = np.arange(n_samples)
        rng = np.random.default_rng(seed)

        for _ in range(epochs):
            if shuffle:
                rng.shuffle(idx)
            for start in range(0, n_samples, batch_size):
                batch_idx = idx[start:start + batch_size]
                xb = X_tensor[batch_idx]
                yb = y_tensor[batch_idx]

                optimizer.zero_grad()
                pred = self.model(xb)
                loss = ((pred - yb) ** 2).mean()
                loss.backward()
                optimizer.step()

            with torch.no_grad():
                pred_all = self.model(X_tensor)
                epoch_loss = ((pred_all - y_tensor) ** 2).mean().item()
                pred_labels = torch.argmax(pred_all, dim=1)
                true_labels = torch.argmax(y_tensor, dim=1)
                acc = (pred_labels == true_labels).float().mean().item()

            history["loss"].append(epoch_loss)
            history["accuracy"].append(acc)

        return history

    def forward(self, x, training=False, precision="float32"):
        dtype = torch.float32 if precision == "float32" else torch.float16
        with torch.no_grad():
            xt = torch.from_numpy(x.astype(np.float32)).to(self.device)
            if dtype == torch.float16:
                xt = xt.half()
                self.model.half()
            else:
                self.model.float()
            out = self.model(xt)
            return out.float().cpu().numpy()

    def predict(self, x, precision="float32"):
        out = self.forward(x, training=False, precision=precision)
        return np.argmax(out, axis=1)
