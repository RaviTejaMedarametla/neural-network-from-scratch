"""Shared data and initialization helpers."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def one_hot(y: np.ndarray, n_classes: int | None = None) -> np.ndarray:
    labels = y.astype(int).ravel()
    classes = int(labels.max() + 1) if n_classes is None else int(n_classes)
    out = np.zeros((labels.shape[0], classes), dtype=np.float32)
    out[np.arange(labels.shape[0]), labels] = 1.0
    return out


def initialize_weights(n_in: int, n_out: int, rng: np.random.Generator | None = None, dtype: np.dtype = np.float32) -> np.ndarray:
    limit = np.sqrt(6.0 / (n_in + n_out))
    sampler = np.random if rng is None else rng
    weights = sampler.uniform(-limit, limit, (n_in, n_out))
    return weights.astype(dtype)


def custom_uniform(min_value: float, max_value: float, shape: tuple[int, ...], seed: int = 3042022) -> np.ndarray:
    rnd = np.random.default_rng(seed)
    return rnd.uniform(min_value, max_value, shape)


def get_list(s: str) -> tuple[list[Any], str | None]:
    index_from = s.find("[")
    index_to = s.find("]")
    data_str = s[index_from : index_to + 1]
    data_list = ast.literal_eval(data_str)
    if index_to + 2 > len(s):
        return data_list, None
    return data_list, s[index_to + 2 :]


def full_check(result: list[float], true_result: list[float], name: str, tolerance: float = 0.05) -> tuple[bool, str]:
    if not isinstance(result, list):
        return False, f"Output for {name} is not a list."
    if len(result) != len(true_result):
        return False, f"Output for {name} should contain {len(true_result)} values, found {len(result)}."

    for value, true_value in zip(result, true_result):
        if true_value == 0:
            if abs(value - true_value) > tolerance:
                return False, f"Incorrect {name} values. Check your {name} function."
        elif not (abs((value - true_value) / true_value) < tolerance):
            return False, f"Incorrect {name} values. Check your {name} function."

    return True, ""


def load_fashion_mnist_split(csv_path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    raw = pd.read_csv(csv_path)
    X = raw[raw.columns[1:]].values.astype(np.float32)
    X = X / max(np.max(X), 1.0)
    y = one_hot(raw["label"].values)
    return X, y


def get_train() -> tuple[np.ndarray, np.ndarray]:
    return load_fashion_mnist_split("neural_network_from_scratch/Data/fashion-mnist_train.csv")


def get_test() -> tuple[np.ndarray, np.ndarray]:
    return load_fashion_mnist_split("neural_network_from_scratch/Data/fashion-mnist_test.csv")
