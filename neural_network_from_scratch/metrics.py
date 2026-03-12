"""Model correctness and performance metrics utilities.

This module centralizes evaluation logic so experiments can report consistent
quality and runtime measurements across precision modes and hardware targets.
"""

from __future__ import annotations

import time
import tracemalloc
from dataclasses import dataclass

import numpy as np

from neural_network_from_scratch.metrics_helpers import compute_classification_stats, summarize_inference_performance


@dataclass(frozen=True)
class PerformanceMetrics:
    """Latency/throughput/memory metrics for a forward pass workload."""

    latency_per_sample_s: float
    throughput_samples_per_s: float
    peak_memory_mb: float
    total_runtime_s: float


@dataclass(frozen=True)
class CorrectnessMetrics:
    """Classification quality metrics for integer class labels."""

    accuracy: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    confusion_matrix: np.ndarray


def _as_label_vector(y: np.ndarray) -> np.ndarray:
    """Convert integer labels or one-hot labels to a 1D class vector."""
    y = np.asarray(y)
    if y.ndim == 1:
        return y.astype(np.int64)
    if y.ndim == 2:
        return np.argmax(y, axis=1).astype(np.int64)
    raise ValueError("labels must be a 1D integer array or a 2D one-hot array")


def _confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, n_classes: int) -> np.ndarray:
    cm = np.zeros((n_classes, n_classes), dtype=np.int64)
    np.add.at(cm, (y_true, y_pred), 1)
    return cm


def compute_correctness_metrics(y_true: np.ndarray, y_pred: np.ndarray, n_classes: int | None = None) -> CorrectnessMetrics:
    """Compute classification metrics without external dependencies."""
    computed = compute_classification_stats(y_true=y_true, y_pred=y_pred, n_classes=n_classes)
    return CorrectnessMetrics(
        accuracy=computed.accuracy,
        precision_macro=computed.precision_macro,
        recall_macro=computed.recall_macro,
        f1_macro=computed.f1_macro,
        confusion_matrix=computed.confusion_matrix,
    )


def measure_inference_performance(model, X: np.ndarray, precision: str = "float32", runs: int = 10) -> PerformanceMetrics:
    """Measure inference latency, throughput and peak allocated memory."""
    if runs < 1:
        raise ValueError("runs must be >= 1")

    model.forward(X, training=False, precision=precision)

    tracemalloc.start()
    t0 = time.perf_counter()
    timings = []
    try:
        for _ in range(runs):
            run_t0 = time.perf_counter()
            model.forward(X, training=False, precision=precision)
            timings.append(time.perf_counter() - run_t0)
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    total_runtime = time.perf_counter() - t0
    summary = summarize_inference_performance(
        timings_s=timings,
        n_samples=int(X.shape[0]),
        peak_memory_bytes=int(peak_bytes),
        total_runtime_s=float(total_runtime),
    )
    return PerformanceMetrics(
        latency_per_sample_s=summary.latency_per_sample_s,
        throughput_samples_per_s=summary.throughput_samples_per_s,
        peak_memory_mb=summary.peak_memory_mb,
        total_runtime_s=summary.total_runtime_s,
    )


def evaluate_model(model, X: np.ndarray, y_true: np.ndarray, precision: str = "float32", runs: int = 10) -> dict:
    """Return a combined quality/performance report for a model and dataset."""
    predictions = model.predict(X, precision=precision)
    correctness = compute_correctness_metrics(y_true=y_true, y_pred=predictions)
    performance = measure_inference_performance(model=model, X=X, precision=precision, runs=runs)

    return {
        "accuracy": correctness.accuracy,
        "precision_macro": correctness.precision_macro,
        "recall_macro": correctness.recall_macro,
        "f1_macro": correctness.f1_macro,
        "confusion_matrix": correctness.confusion_matrix,
        "latency_per_sample_s": performance.latency_per_sample_s,
        "throughput_samples_per_s": performance.throughput_samples_per_s,
        "peak_memory_mb": performance.peak_memory_mb,
        "total_runtime_s": performance.total_runtime_s,
    }
