"""Canonical metrics schema and backward-compatible normalization utilities."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

CANONICAL_KEYS = {
    "generated_at_utc",
    "epochs",
    "batch_size",
    "learning_rate",
    "seed",
    "dataset",
    "bad_metrics",
    "test_accuracy_percent",
    "training_time_seconds",
    "peak_memory_mb",
    "final_epoch_loss",
    "quality_gate_reason",
    "error",
}

KEY_ALIASES: dict[str, tuple[str, ...]] = {
    "dataset": ("data_source",),
    "training_time_seconds": ("train_time_seconds",),
}


def _first_present(payload: Mapping[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
    return None


def normalize_metrics_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a canonical metrics payload while accepting legacy key aliases."""
    normalized = dict(payload)

    for canonical_key, aliases in KEY_ALIASES.items():
        value = _first_present(payload, (canonical_key, *aliases))
        if value is not None:
            normalized[canonical_key] = value

    return normalized
