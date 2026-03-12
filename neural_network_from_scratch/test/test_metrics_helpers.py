import numpy as np

from neural_network_from_scratch.metrics_helpers import compute_classification_stats, summarize_inference_performance


def test_compute_classification_stats_expected_values():
    y_true = np.array([0, 1, 2, 2, 1, 0])
    y_pred = np.array([0, 1, 1, 2, 1, 2])

    stats = compute_classification_stats(y_true=y_true, y_pred=y_pred, n_classes=3)

    np.testing.assert_allclose(stats.accuracy, 4 / 6)
    np.testing.assert_allclose(stats.precision_macro, (1.0 + (2 / 3) + 0.5) / 3)
    np.testing.assert_allclose(stats.recall_macro, (0.5 + 1.0 + 0.5) / 3)
    assert stats.confusion_matrix.tolist() == [[1, 0, 1], [0, 2, 0], [0, 1, 1]]


def test_summarize_inference_performance_is_deterministic_for_fixed_inputs():
    summary = summarize_inference_performance(
        timings_s=[0.20, 0.10, 0.10],
        n_samples=50,
        peak_memory_bytes=1048576,
        total_runtime_s=0.42,
    )

    np.testing.assert_allclose(summary.latency_per_sample_s, (0.4 / 3) / 50)
    np.testing.assert_allclose(summary.throughput_samples_per_s, 50 / (0.4 / 3))
    np.testing.assert_allclose(summary.peak_memory_mb, 1.0)
    np.testing.assert_allclose(summary.total_runtime_s, 0.42)
