import numpy as np

from neural_network_from_scratch import NeuralNetwork


def test_predict_shape_and_binary_output():
    x = np.random.default_rng(0).normal(size=(10, 3))
    model = NeuralNetwork(n_features=3, seed=1)
    y = model.predict(x)
    assert y.shape == (10,)
    assert set(np.unique(y)).issubset({0, 1})


def test_fit_improves_simple_problem():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(200, 2))
    y = (x[:, 0] + x[:, 1] > 0).astype(np.int64)

    model = NeuralNetwork(n_features=2, n_hidden=12, lr=0.2, seed=3)
    before = (model.predict(x) == y).mean()
    model.fit(x, y, epochs=200)
    after = (model.predict(x) == y).mean()

    assert after >= before
    assert after > 0.85
