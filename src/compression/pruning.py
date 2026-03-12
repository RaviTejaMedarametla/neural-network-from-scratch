from __future__ import annotations

import numpy as np


class Pruner:
    """Model pruning helper supporting global magnitude pruning."""

    def __init__(self, model) -> None:
        self.model = model
        self.masks: dict[str, np.ndarray] = {}

    def _all_param_views(self) -> list[tuple[str, np.ndarray]]:
        out: list[tuple[str, np.ndarray]] = []
        for name, p in self.model.named_parameters():
            out.append((name, p["param"]))
        return out

    def magnitude_prune(self, sparsity: float) -> None:
        if not 0 <= sparsity < 1:
            raise ValueError("sparsity must be in [0,1)")
        params = self._all_param_views()
        all_weights = np.concatenate([w.ravel() for _, w in params]) if params else np.array([0.0])
        threshold = np.percentile(np.abs(all_weights), sparsity * 100)
        for name, w in params:
            mask = np.abs(w) > threshold
            self.masks[name] = mask
            w *= mask

    def structured_prune_channels(self, layer_index: int, sparsity: float, norm: int = 2) -> None:
        layer = self.model.layers[layer_index]
        if not hasattr(layer, "w"):
            raise ValueError("layer does not have weight matrix/tensor")
        w = layer.w
        if w.ndim == 2:
            channel_norms = np.linalg.norm(w, ord=norm, axis=0)
            threshold = np.percentile(channel_norms, sparsity * 100)
            keep = channel_norms > threshold
            mask = np.ones_like(w)
            mask[:, ~keep] = 0
            layer.w *= mask
            self.masks[f"layer{layer_index}.channels"] = mask
        elif w.ndim == 4:
            channel_norms = np.linalg.norm(w.reshape(w.shape[0], -1), ord=norm, axis=1)
            threshold = np.percentile(channel_norms, sparsity * 100)
            keep = channel_norms > threshold
            mask = np.zeros_like(w)
            mask[keep] = 1.0
            layer.w *= mask
            self.masks[f"layer{layer_index}.channels"] = mask

    def apply_masks(self) -> None:
        for name, p in self.model.named_parameters():
            if name in self.masks:
                p["param"] *= self.masks[name]

    def remove_pruning(self) -> None:
        self.masks = {}
