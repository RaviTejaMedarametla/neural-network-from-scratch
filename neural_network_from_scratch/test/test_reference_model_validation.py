import numpy as np
import pytest

from neural_network_from_scratch.model import NeuralNetwork


def test_reference_model_initialization_is_deterministic_with_seed():
    a = NeuralNetwork(layer_sizes=[4, 6, 3], learning_rate=0.01, seed=17)
    b = NeuralNetwork(layer_sizes=[4, 6, 3], learning_rate=0.01, seed=17)

    for wa, wb in zip(a.weights, b.weights):
        np.testing.assert_allclose(wa, wb)


def test_forward_rejects_invalid_feature_shape():
    model = NeuralNetwork(layer_sizes=[3, 5, 2], learning_rate=0.01, seed=1)

    with pytest.raises(ValueError, match="2D array"):
        model.forward(np.array([1.0, 2.0, 3.0]))

    with pytest.raises(ValueError, match="expects 3"):
        model.forward(np.ones((8, 4)))


def test_train_step_rejects_bad_labels():
    model = NeuralNetwork(layer_sizes=[3, 4, 2], learning_rate=0.01, seed=2)
    x = np.ones((5, 3), dtype=np.float64)

    with pytest.raises(ValueError, match="same number of samples"):
        model.train_step(x, np.array([0, 1]))

    with pytest.raises(ValueError, match=r"must be in \[0, 1\]"):
        model.train_step(x, np.array([0, 1, 0, 1, 2]))
