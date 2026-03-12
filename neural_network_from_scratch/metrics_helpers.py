"""Helper functions for model correctness and performance metric computations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ComputedCorrectness:
    accuracy: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    confusion_matrix: np.ndarray


@dataclass(frozen=True)
class ComputedPerformance:
    latency_per_sample_s: float
    throughput_samples_per_s: float
    peak_memory_mb: float
    total_runtime_s: float


def as_label_vector(y: np.ndarray) -> np.ndarray:
    """Convert 1D integer labels or 2D one-hot labels to a 1D class vector."""
    y = np.asarray(y)
    if y.ndim == 1:
        return y.astype(np.int64)
    if y.ndim == 2:
        return np.argmax(y, axis=1).astype(np.int64)
    raise ValueError("labels must be a 1D integer array or a 2D one-hot array")


def build_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, n_classes: int) -> np.ndarray:
    cm = np.zeros((n_classes, n_classes), dtype=np.int64)
    np.add.at(cm, (y_true, y_pred), 1)
    return cm


def compute_classification_stats(y_true: np.ndarray, y_pred: np.ndarray, n_classes: int | None = None) -> ComputedCorrectness:
    y_true_labels = as_label_vector(y_true)
    y_pred_labels = as_label_vector(y_pred)

    if y_true_labels.shape != y_pred_labels.shape:
        raise ValueError("y_true and y_pred must have matching shapes after label conversion")

    if n_classes is None:
        n_classes = int(max(y_true_labels.max(initial=0), y_pred_labels.max(initial=0)) + 1)

    cm = build_confusion_matrix(y_true_labels, y_pred_labels, n_classes)

    true_positive = np.diag(cm).astype(np.float64)
    predicted_positive = np.sum(cm, axis=0).astype(np.float64)
    actual_positive = np.sum(cm, axis=1).astype(np.float64)

    precision_per_class = np.divide(true_positive, predicted_positive, out=np.zeros_like(true_positive), where=predicted_positive > 0)
    recall_per_class = np.divide(true_positive, actual_positive, out=np.zeros_like(true_positive), where=actual_positive > 0)
    f1_per_class = np.divide(
        2 * precision_per_class * recall_per_class,
        precision_per_class + recall_per_class,
        out=np.zeros_like(precision_per_class),
        where=(precision_per_class + recall_per_class) > 0,
    )

    accuracy = float(np.mean(y_true_labels == y_pred_labels))
    return ComputedCorrectness(
        accuracy=accuracy,
        precision_macro=float(np.mean(precision_per_class)),
        recall_macro=float(np.mean(recall_per_class)),
        f1_macro=float(np.mean(f1_per_class)),
        confusion_matrix=cm,
    )


def summarize_inference_performance(timings_s: list[float], n_samples: int, peak_memory_bytes: int, total_runtime_s: float) -> ComputedPerformance:
    if not timings_s:
        raise ValueError("timings_s must not be empty")
    if n_samples < 1:
        raise ValueError("n_samples must be >= 1")

    avg_latency = float(np.mean(timings_s))
    latency_per_sample = avg_latency / n_samples
    throughput = n_samples / avg_latency if avg_latency > 0 else float("inf")

    return ComputedPerformance(
        latency_per_sample_s=float(latency_per_sample),
        throughput_samples_per_s=float(throughput),
        peak_memory_mb=float(peak_memory_bytes / (1024 * 1024)),
        total_runtime_s=float(total_runtime_s),
    )
