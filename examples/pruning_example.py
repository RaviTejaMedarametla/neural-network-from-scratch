import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

np.random.seed(7)

from src.compression.pruning import Pruner
from src.compression.sparsity import sparsity_ratio
from src.layers import Dense
from src.losses.cross_entropy import CrossEntropyLoss
from src.models.sequential import Sequential
from src.optimizers.sgd import SGD


def main() -> None:
    model = Sequential([Dense(32, 64), Dense(64, 10)])
    x = np.random.randn(256, 32).astype(np.float32)
    y = np.random.randint(0, 10, size=(256,))

    opt = SGD(model.parameters(), lr=1e-2)
    loss_fn = CrossEntropyLoss()
    for _ in range(2):
        logits = model.forward(x)
        _, grad = loss_fn.forward(logits, y)
        model.backward(grad)
        opt.step()
        opt.zero_grad()

    pruner = Pruner(model)
    pruner.magnitude_prune(0.5)
    pruner.apply_masks()

    for i, layer in enumerate(model.layers):
        if hasattr(layer, "w"):
            print(f"layer{i} sparsity={sparsity_ratio(layer.w):.3f}")


if __name__ == "__main__":
    main()
