from __future__ import annotations

from dataclasses import dataclass
import itertools
from typing import Any

import numpy as np

from src.layers import Dense, MaxPool2D
from src.models.sequential import Sequential


@dataclass
class Operation:
    name: str
    params: dict[str, Any]


class SearchSpace:
    def __init__(self, operations: list[Operation], num_layers: int) -> None:
        self.operations = operations
        self.num_layers = num_layers

    def enumerate(self) -> list[tuple[Operation, ...]]:
        return list(itertools.product(self.operations, repeat=self.num_layers))

    def sample(self, rng: np.random.Generator) -> list[Operation]:
        return [self.operations[int(rng.integers(0, len(self.operations)))] for _ in range(self.num_layers)]


class Architecture:
    def __init__(self, layers: list[Operation]) -> None:
        self.layers = layers

    def build_model(self, input_shape: tuple[int, ...]) -> Sequential:
        model = Sequential()
        in_features = input_shape[-1]
        for op in self.layers:
            if op.name == "dense":
                out_features = int(op.params.get("out_features", in_features))
                model.add(Dense(in_features, out_features))
                in_features = out_features
            elif op.name == "maxpool":
                model.add(MaxPool2D(pool_size=int(op.params.get("pool_size", 2))))
            elif op.name == "identity":
                continue
        return model

    def signature(self) -> str:
        return "|".join([f"{op.name}:{sorted(op.params.items())}" for op in self.layers])
