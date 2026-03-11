#!/usr/bin/env python3
"""Collect model metrics for CI and local benchmarking.

Design goals:
- Deterministic, dependency-light, and network-optional.
- Emit one stable JSON schema even on failure.
- Preserve compatibility aliases for older payload consumers.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import tracemalloc
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from neural_network_from_scratch.metrics_schema import (
    KEY_ACCURACY,
    KEY_BAD_METRICS,
    KEY_DATASET,
    KEY_DATA_SOURCE,
    KEY_PEAK_MEMORY_MB,
    KEY_TRAIN_TIME,
    KEY_TRAIN_TIME_ALIAS,
    with_compatibility_aliases,
)
from neural_network_from_scratch.model import NeuralNetwork


@dataclass
class RunConfig:
    epochs: int = 5
    batch_size: int = 64
    learning_rate: float = 0.01
    seed: int = 42
    data_dir: Path = Path("neural_network_from_scratch/Data")
    max_train: int = 6000
    max_test: int = 1000
    min_acceptable_accuracy: float = 80.0
    output: Path = Path("metrics.json")
    no_synthetic_fallback: bool = False


@dataclass
class DatasetBundle:
    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray
    source: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_config(cfg: RunConfig) -> None:
    if cfg.epochs < 1:
        raise ValueError("epochs must be >= 1")
    if cfg.batch_size < 1:
        raise ValueError("batch_size must be >= 1")
    if cfg.learning_rate <= 0:
        raise ValueError("learning_rate must be > 0")
    if cfg.max_train < 1 or cfg.max_test < 1:
        raise ValueError("max_train and max_test must be >= 1")


def _is_numeric_row(row: list[str]) -> bool:
    if not row:
        return False
    try:
        for value in row:
            float(value)
    except ValueError:
        return False
    return True


def _read_csv_rows(path: Path, max_rows: int | None) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")

    rows: list[list[float]] = []
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.reader(fp)
        first_row = next(reader, None)
        if first_row is None:
            raise ValueError(f"empty CSV: {path}")

        # Accept either header+data or headerless numeric CSV.
        if _is_numeric_row(first_row):
            rows.append([float(v) for v in first_row])

        for row in reader:
            if not row:
                continue
            if not _is_numeric_row(row):
                raise ValueError(f"non-numeric row in {path}: {row[:3]}...")
            rows.append([float(v) for v in row])

            if max_rows is not None and len(rows) >= max_rows:
                break

    if not rows:
        raise ValueError(f"CSV has no numeric data rows: {path}")

    arr = np.asarray(rows, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[1] < 2:
        raise ValueError(f"expected label + features columns in {path}, got shape={arr.shape}")
    return arr


def load_fashion_mnist_csv(data_dir: Path, max_train: int | None, max_test: int | None) -> DatasetBundle:
    train_arr = _read_csv_rows(data_dir / "fashion-mnist_train.csv", max_train)
    test_arr = _read_csv_rows(data_dir / "fashion-mnist_test.csv", max_test)

    y_train = train_arr[:, 0].astype(np.int64)
    x_train = (train_arr[:, 1:] / 255.0).astype(np.float64)
    y_test = test_arr[:, 0].astype(np.int64)
    x_test = (test_arr[:, 1:] / 255.0).astype(np.float64)

    if x_train.shape[1] != x_test.shape[1]:
        raise ValueError("train/test feature dimensions do not match")

    return DatasetBundle(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, source="fashion-mnist-local-csv")


def make_synthetic_bundle(seed: int, n_train: int = 4000, n_test: int = 800, n_features: int = 784, n_classes: int = 10) -> DatasetBundle:
    rng = np.random.default_rng(seed)
    x_train = rng.normal(size=(n_train, n_features))
    x_test = rng.normal(size=(n_test, n_features))

    teacher_w = rng.normal(size=(n_features, n_classes))
    y_train = np.argmax(x_train @ teacher_w, axis=1).astype(np.int64)
    y_test = np.argmax(x_test @ teacher_w, axis=1).astype(np.int64)

    return DatasetBundle(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, source="synthetic-fallback")


def _iter_minibatches(x: np.ndarray, y: np.ndarray, batch_size: int, rng: np.random.Generator) -> Iterable[tuple[np.ndarray, np.ndarray]]:
    indices = rng.permutation(x.shape[0])
    x_epoch = x[indices]
    y_epoch = y[indices]
    for start in range(0, x.shape[0], batch_size):
        end = min(start + batch_size, x.shape[0])
        yield x_epoch[start:end], y_epoch[start:end]


def train_and_measure(bundle: DatasetBundle, cfg: RunConfig) -> dict:
    n_classes = int(np.max(bundle.y_train) + 1)
    model = NeuralNetwork(
        layer_sizes=[bundle.x_train.shape[1], 128, 64, n_classes],
        learning_rate=cfg.learning_rate,
        seed=cfg.seed,
    )

    rng = np.random.default_rng(cfg.seed)
    tracemalloc.start()
    t0 = time.perf_counter()

    final_epoch_loss = 0.0
    for _ in range(cfg.epochs):
        cumulative_loss = 0.0
        for xb, yb in _iter_minibatches(bundle.x_train, bundle.y_train, cfg.batch_size, rng):
            batch_loss = model.train_step(xb, yb)
            cumulative_loss += float(batch_loss) * len(xb)
        final_epoch_loss = cumulative_loss / bundle.x_train.shape[0]

    duration_s = time.perf_counter() - t0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    acc = model.accuracy(bundle.x_test, bundle.y_test) * 100.0

    return {
        KEY_ACCURACY: float(acc),
        KEY_TRAIN_TIME_ALIAS: float(duration_s),
        KEY_TRAIN_TIME: float(duration_s),
        KEY_PEAK_MEMORY_MB: float(peak_bytes / (1024**2)),
        "final_epoch_loss": float(final_epoch_loss),
        "epochs": int(cfg.epochs),
        "batch_size": int(cfg.batch_size),
        "n_train_samples": int(bundle.x_train.shape[0]),
        "n_test_samples": int(bundle.x_test.shape[0]),
        "n_features": int(bundle.x_train.shape[1]),
        "n_classes": int(np.max(bundle.y_train) + 1),
    }


def build_failure_payload(cfg: RunConfig, message: str, source: str = "unknown") -> dict:
    payload = {
        "generated_at_utc": _utc_now(),
        KEY_BAD_METRICS: True,
        "error": message,
        "quality_gate_reason": message,
        KEY_DATA_SOURCE: source,
        KEY_DATASET: source,
        "seed": int(cfg.seed),
        "epochs": int(cfg.epochs),
        "batch_size": int(cfg.batch_size),
        "learning_rate": float(cfg.learning_rate),
        KEY_ACCURACY: 0.0,
        KEY_TRAIN_TIME_ALIAS: 0.0,
        KEY_TRAIN_TIME: 0.0,
        KEY_PEAK_MEMORY_MB: 0.0,
        "final_epoch_loss": 0.0,
    }
    return with_compatibility_aliases(payload)


def collect_metrics(cfg: RunConfig) -> dict:
    try:
        validate_config(cfg)
    except Exception as exc:
        return build_failure_payload(cfg, f"invalid config: {exc}")

    base = {
        "generated_at_utc": _utc_now(),
        KEY_BAD_METRICS: False,
        "seed": int(cfg.seed),
        "epochs": int(cfg.epochs),
        "batch_size": int(cfg.batch_size),
        "learning_rate": float(cfg.learning_rate),
    }

    try:
        bundle = load_fashion_mnist_csv(cfg.data_dir, cfg.max_train, cfg.max_test)
    except Exception as exc:
        if cfg.no_synthetic_fallback:
            return build_failure_payload(cfg, f"dataset load failed and fallback disabled: {exc}")
        bundle = make_synthetic_bundle(seed=cfg.seed, n_train=cfg.max_train, n_test=cfg.max_test)

    measured = train_and_measure(bundle, cfg)
    payload = {**base, **measured}
    payload[KEY_DATA_SOURCE] = bundle.source
    payload[KEY_DATASET] = bundle.source
    payload = with_compatibility_aliases(payload)

    if payload[KEY_ACCURACY] < cfg.min_acceptable_accuracy:
        payload[KEY_BAD_METRICS] = True
        payload["quality_gate_reason"] = (
            f"accuracy {payload[KEY_ACCURACY]:.4f}% < {cfg.min_acceptable_accuracy:.2f}%"
        )

    return payload


def write_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(description="Collect NN metrics into a JSON payload.")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--data-dir", type=Path, default=Path("neural_network_from_scratch/Data"))
    parser.add_argument("--max-train", type=int, default=6000)
    parser.add_argument("--max-test", type=int, default=1000)
    parser.add_argument("--min-acceptable-accuracy", type=float, default=80.0)
    parser.add_argument("--output", type=Path, default=Path("metrics.json"))
    parser.add_argument("--no-synthetic-fallback", action="store_true")
    ns = parser.parse_args()

    return RunConfig(
        epochs=ns.epochs,
        batch_size=ns.batch_size,
        learning_rate=ns.learning_rate,
        seed=ns.seed,
        data_dir=ns.data_dir,
        max_train=ns.max_train,
        max_test=ns.max_test,
        min_acceptable_accuracy=ns.min_acceptable_accuracy,
        output=ns.output,
        no_synthetic_fallback=ns.no_synthetic_fallback,
    )


def main() -> int:
    cfg = parse_args()
    payload = collect_metrics(cfg)
    write_payload(cfg.output, payload)
    print(f"[collect_metrics] wrote metrics payload to {cfg.output}")
    if payload.get(KEY_BAD_METRICS):
        print(f"[collect_metrics] warning: {payload.get('quality_gate_reason', payload.get('error', 'bad metrics'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
