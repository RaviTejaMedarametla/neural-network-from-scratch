from __future__ import annotations
import numpy as np


def save_parameters(params: list[dict], path: str) -> None:
    arrays = {f"arr_{i}": p["param"] for i, p in enumerate(params)}
    np.savez(path, **arrays)


def load_parameters(params: list[dict], path: str) -> None:
    data = np.load(path)
    for i, p in enumerate(params):
        p["param"][:] = data[f"arr_{i}"]
