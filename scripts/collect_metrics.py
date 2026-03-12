#!/usr/bin/env python3
"""Collect training metrics and persist them as JSON.

This script is CI-oriented and intentionally resilient:
- it accepts workflow arguments used in `.github/workflows/update-metrics.yml`
- it prefers local Fashion-MNIST CSV data to avoid network-only dependencies
- it can optionally synthesize a small dataset fallback
- it always attempts to write an output metrics JSON payload
"""

from __future__ import annotations

import argparse
import json
import os
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from neural_network_from_scratch.model import NeuralNetwork
from neural_network_from_scratch.metrics_schema import normalize_metrics_payload


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _detect_cpu_count() -> int:
    return max(1, int(os.cpu_count() or 1))


def _resolve_batch_size(requested_batch_size: int, n_samples: int, cpu_count: int, auto_optimize: bool) -> int:
    requested = max(1, int(requested_batch_size))
    if not auto_optimize:
        return requested

    # Deterministic CPU-aware heuristic: increase batch size for larger machines.
    if cpu_count >= 16:
        tuned = max(requested, 256)
    elif cpu_count >= 8:
        tuned = max(requested, 128)
    elif cpu_count >= 4:
        tuned = max(requested, 96)
    else:
        tuned = requested

    return min(tuned, max(1, int(n_samples)))


def _load_fashion_mnist_from_repo(data_dir: Path, max_train: int | None = None, max_test: int | None = None):
    train_csv = data_dir / "fashion-mnist_train.csv"
    test_csv = data_dir / "fashion-mnist_test.csv"
    if not train_csv.exists() or not test_csv.exists():
        raise FileNotFoundError(f"missing Fashion-MNIST CSVs under {data_dir}")

    train = np.loadtxt(train_csv, delimiter=",", skiprows=1)
    test = np.loadtxt(test_csv, delimiter=",", skiprows=1)

    if max_train is not None:
        train = train[:max_train]
    if max_test is not None:
        test = test[:max_test]

    y_train = train[:, 0].astype(np.int64)
    X_train = (train[:, 1:] / 255.0).astype(np.float64)
    y_test = test[:, 0].astype(np.int64)
    X_test = (test[:, 1:] / 255.0).astype(np.float64)
    return X_train, X_test, y_train, y_test


def _make_synthetic_data(seed: int, n_train: int = 4000, n_test: int = 800, n_features: int = 784, n_classes: int = 10):
    rng = np.random.default_rng(seed)
    X_train = rng.normal(size=(n_train, n_features))
    X_test = rng.normal(size=(n_test, n_features))

    # Lightweight linear teacher for learnable labels.
    teacher_w = rng.normal(size=(n_features, n_classes))
    y_train = np.argmax(X_train @ teacher_w, axis=1).astype(np.int64)
    y_test = np.argmax(X_test @ teacher_w, axis=1).astype(np.int64)
    return X_train, X_test, y_train, y_test


def _run_training(X_train, y_train, X_test, y_test, epochs: int, batch_size: int, learning_rate: float, seed: int):
    model = NeuralNetwork(layer_sizes=[X_train.shape[1], 128, 64, int(np.max(y_train) + 1)], learning_rate=learning_rate, seed=seed)

    n_samples = X_train.shape[0]
    rng = np.random.default_rng(seed)

    tracemalloc.start()
    t0 = time.perf_counter()

    final_epoch_loss = None
    for _ in range(epochs):
        indices = rng.permutation(n_samples)
        X_epoch = X_train[indices]
        y_epoch = y_train[indices]

        epoch_loss = 0.0
        for i in range(0, n_samples, batch_size):
            X_batch = X_epoch[i : i + batch_size]
            y_batch = y_epoch[i : i + batch_size]
            loss = model.train_step(X_batch, y_batch)
            epoch_loss += float(loss) * len(X_batch)
        final_epoch_loss = epoch_loss / n_samples

    train_time_s = time.perf_counter() - t0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    test_acc = model.accuracy(X_test, y_test) * 100.0

    return {
        "test_accuracy_percent": float(test_acc),
        "training_time_seconds": float(train_time_s),
        "peak_memory_mb": float(peak_bytes / (1024**2)),
        "final_epoch_loss": float(final_epoch_loss if final_epoch_loss is not None else 0.0),
    }


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect training metrics into JSON.")
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
    parser.add_argument("--auto-optimize-batch-size", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    cpu_count = _detect_cpu_count()
    payload = {
        "generated_at_utc": _timestamp(),
        "epochs": int(args.epochs),
        "batch_size": int(args.batch_size),
        "learning_rate": float(args.learning_rate),
        "seed": int(args.seed),
        "dataset": "unknown",
        "bad_metrics": False,
        "hardware_context": {
            "cpu_count": cpu_count,
            "auto_optimized_batch_size": bool(args.auto_optimize_batch_size),
        },
    }

    try:
        X_train, X_test, y_train, y_test = _load_fashion_mnist_from_repo(
            data_dir=args.data_dir,
            max_train=args.max_train,
            max_test=args.max_test,
        )
        payload["dataset"] = "fashion-mnist-local-csv"
    except Exception as exc:
        if args.no_synthetic_fallback:
            payload.update(
                {
                    "bad_metrics": True,
                    "error": f"dataset load failed and fallback disabled: {exc}",
                    "test_accuracy_percent": 0.0,
                    "training_time_seconds": 0.0,
                    "peak_memory_mb": 0.0,
                }
            )
            _write_json(args.output, normalize_metrics_payload(payload))
            print(f"[collect_metrics] warning: {payload['error']}")
            return 0

        X_train, X_test, y_train, y_test = _make_synthetic_data(seed=args.seed)
        payload["dataset"] = "synthetic-fallback"

    resolved_batch_size = _resolve_batch_size(
        requested_batch_size=int(args.batch_size),
        n_samples=int(X_train.shape[0]),
        cpu_count=cpu_count,
        auto_optimize=bool(args.auto_optimize_batch_size),
    )
    payload["batch_size"] = resolved_batch_size
    payload["hardware_context"]["resolved_batch_size"] = int(resolved_batch_size)

    try:
        measured = _run_training(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            epochs=args.epochs,
            batch_size=resolved_batch_size,
            learning_rate=args.learning_rate,
            seed=args.seed,
        )
        payload.update(measured)

        if payload["test_accuracy_percent"] < args.min_acceptable_accuracy:
            payload["bad_metrics"] = True
            payload["quality_gate_reason"] = (
                f"accuracy {payload['test_accuracy_percent']:.4f}% < {args.min_acceptable_accuracy:.2f}%"
            )
    except Exception as exc:
        payload.update(
            {
                "bad_metrics": True,
                "error": f"training/evaluation failed: {exc}",
                "test_accuracy_percent": 0.0,
                "training_time_seconds": 0.0,
                "peak_memory_mb": 0.0,
            }
        )

    _write_json(args.output, normalize_metrics_payload(payload))
    print(f"[collect_metrics] wrote metrics to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
