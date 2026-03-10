import numpy as np

from neural_network_from_scratch.metrics import compute_correctness_metrics, evaluate_model, measure_inference_performance
from neural_network_from_scratch.student import TwoLayerNeural


def test_compute_correctness_metrics_matches_expected_values():
    y_true = np.array([0, 1, 2, 2, 1, 0])
    y_pred = np.array([0, 1, 1, 2, 1, 2])

    metrics = compute_correctness_metrics(y_true, y_pred, n_classes=3)

    assert metrics.confusion_matrix.shape == (3, 3)
    np.testing.assert_allclose(metrics.accuracy, 4 / 6)
    np.testing.assert_allclose(metrics.precision_macro, (1.0 + (2 / 3) + 0.5) / 3)
    np.testing.assert_allclose(metrics.recall_macro, (0.5 + 1.0 + 0.5) / 3)


def test_measure_inference_performance_returns_positive_values():
    rng = np.random.default_rng(13)
    x = rng.normal(size=(64, 3)).astype(np.float32)
    y = (x[:, 0] > 0).astype(int)

    model = TwoLayerNeural(3, 2, hidden_activation='relu', output_activation='softmax')
    model.fit(x, y, epochs=5, alpha=0.1, batch_size=16, seed=13)

    perf = measure_inference_performance(model, x, precision='float32', runs=3)
    assert perf.latency_per_sample_s > 0
    assert perf.throughput_samples_per_s > 0
    assert perf.peak_memory_mb >= 0


def test_evaluate_model_contains_correctness_and_performance_sections():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(120, 4)).astype(np.float32)
    y = (x[:, 0] + x[:, 1] > 0).astype(int)

    model = TwoLayerNeural(4, 2, hidden_activation='relu', output_activation='softmax')
    model.fit(x, y, epochs=15, alpha=0.15, batch_size=32, seed=4)

    report = evaluate_model(model, x, y, precision='float32', runs=2)

    assert set([
        'accuracy',
        'precision_macro',
        'recall_macro',
        'f1_macro',
        'confusion_matrix',
        'latency_per_sample_s',
        'throughput_samples_per_s',
        'peak_memory_mb',
        'total_runtime_s',
    ]).issubset(report.keys())
    assert report['accuracy'] >= 0.8
    assert report['confusion_matrix'].shape == (2, 2)
