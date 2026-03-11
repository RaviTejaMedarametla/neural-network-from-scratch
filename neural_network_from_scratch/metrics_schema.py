"""Shared metrics payload schema helpers.

Centralizing key names avoids drift across collection, reporting, and README
publishing scripts.
"""

from __future__ import annotations

from typing import Any

KEY_ACCURACY = "test_accuracy_percent"
KEY_TRAIN_TIME = "training_time_seconds"
KEY_TRAIN_TIME_ALIAS = "train_time_seconds"
KEY_PEAK_MEMORY_MB = "peak_memory_mb"
KEY_DATASET = "dataset"
KEY_DATA_SOURCE = "data_source"
KEY_BAD_METRICS = "bad_metrics"


def get_dataset_source(metrics: dict[str, Any], default: str = "") -> str:
    return str(metrics.get(KEY_DATASET, metrics.get(KEY_DATA_SOURCE, default)))


def get_training_time_seconds(metrics: dict[str, Any], default: Any = None) -> Any:
    return metrics.get(KEY_TRAIN_TIME, metrics.get(KEY_TRAIN_TIME_ALIAS, default))


def with_compatibility_aliases(payload: dict[str, Any]) -> dict[str, Any]:
    """Ensure both old/new alias keys are present for compatibility."""
    out = dict(payload)

    if KEY_DATASET in out and KEY_DATA_SOURCE not in out:
        out[KEY_DATA_SOURCE] = out[KEY_DATASET]
    if KEY_DATA_SOURCE in out and KEY_DATASET not in out:
        out[KEY_DATASET] = out[KEY_DATA_SOURCE]

    if KEY_TRAIN_TIME in out and KEY_TRAIN_TIME_ALIAS not in out:
        out[KEY_TRAIN_TIME_ALIAS] = out[KEY_TRAIN_TIME]
    if KEY_TRAIN_TIME_ALIAS in out and KEY_TRAIN_TIME not in out:
        out[KEY_TRAIN_TIME] = out[KEY_TRAIN_TIME_ALIAS]

    return out
