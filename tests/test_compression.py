import numpy as np

from src.compression.pruning import Pruner
from src.compression.sparsity import sparsity_ratio
from src.layers import Dense
from src.models.sequential import Sequential


def test_magnitude_prune_reaches_target_sparsity():
    model = Sequential([Dense(16, 16)])
    pruner = Pruner(model)
    pruner.magnitude_prune(0.5)
    p = model.layers[0].w
    assert sparsity_ratio(p) >= 0.45
