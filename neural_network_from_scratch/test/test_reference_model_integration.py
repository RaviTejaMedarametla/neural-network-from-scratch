import numpy as np

from neural_network_from_scratch.metrics import evaluate_model
from neural_network_from_scratch.model import NeuralNetwork


def test_reference_model_fit_is_deterministic_for_same_seed():
    rng = np.random.default_rng(123)
    x = rng.normal(size=(100, 4))
    y = (x[:, 0] + 0.5 * x[:, 1] > 0).astype(np.int64)

    a = NeuralNetwork([4, 8, 2], learning_rate=0.05, seed=10)
    b = NeuralNetwork([4, 8, 2], learning_rate=0.05, seed=10)

    hist_a = a.fit(x, y, epochs=6, batch_size=16, shuffle=True, seed=77)
    hist_b = b.fit(x, y, epochs=6, batch_size=16, shuffle=True, seed=77)

    np.testing.assert_allclose(hist_a["loss"], hist_b["loss"])


def test_reference_model_evaluate_model_integration_contract():
    rng = np.random.default_rng(21)
    x = rng.normal(size=(120, 3))
    y = (x[:, 0] - x[:, 1] > 0).astype(np.int64)

    model = NeuralNetwork([3, 10, 2], learning_rate=0.08, seed=4)
    model.fit(x, y, epochs=12, batch_size=24, shuffle=True, seed=4)

    report = evaluate_model(model, x, y, precision="float32", runs=2)

    assert report["confusion_matrix"].shape == (2, 2)
    assert report["accuracy"] >= 0.7
    assert report["throughput_samples_per_s"] > 0
    assert report["latency_per_sample_s"] > 0
