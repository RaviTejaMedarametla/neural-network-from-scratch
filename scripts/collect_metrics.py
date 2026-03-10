#!/usr/bin/env python3
"""Train the NumPy neural network and collect performance metrics."""

from __future__ import annotations

import argparse
import json
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np

from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.dataset_config import (
    FASHION_MNIST_SPEC,
    ensure_dataset_ready,
    load_dataset,
    validate_dataset_file,
)
from neural_network_from_scratch.reproducibility import get_rng, set_global_seed
from neural_network_from_scratch.training import NeuralNetwork


def build_model(seed: int) -> NeuralNetwork:
    precision_cfg = PrecisionConfig(train_dtype="float32", infer_precision="float32", seed=seed)
    return NeuralNetwork(layer_sizes=[784, 64, 10], activations=["relu", "softmax"], precision_config=precision_cfg)


def _load_data(seed: int, allow_synthetic_fallback: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, str]:
    """Load Fashion-MNIST train/test data, with optional synthetic fallback."""
    try:
        ensure_dataset_ready(FASHION_MNIST_SPEC, expected_features=784, expected_min_rows=100, auto_download=True)
        validate_dataset_file(FASHION_MNIST_SPEC.test_path, expected_features=784, expected_min_rows=100)
        X_train, y_train = load_dataset(Path(FASHION_MNIST_SPEC.train_path))
        X_test, y_test = load_dataset(Path(FASHION_MNIST_SPEC.test_path))
        return X_train, y_train, X_test, y_test, FASHION_MNIST_SPEC.name
    except Exception as exc:
        if not allow_synthetic_fallback:
            raise
        rng = get_rng(seed)
        X_train = rng.normal(size=(2048, 784)).astype(np.float32)
        y_train = rng.integers(0, 10, size=2048, dtype=np.int32)
        X_test = rng.normal(size=(512, 784)).astype(np.float32)
        y_test = rng.integers(0, 10, size=512, dtype=np.int32)
        print(f"[collect_metrics] WARNING: falling back to synthetic data due to dataset error: {exc}")
        return X_train, y_train, X_test, y_test, "synthetic-fallback"


def collect_metrics(epochs: int, alpha: float, batch_size: int, seed: int, allow_synthetic_fallback: bool) -> Dict[str, Any]:
    set_global_seed(seed)
    X_train, y_train, X_test, y_test, dataset_name = _load_data(seed, allow_synthetic_fallback)

    model = build_model(seed)
    tracemalloc.start()
    start = time.perf_counter()
    model.fit(X_train, y_train, epochs=epochs, alpha=alpha, batch_size=batch_size, seed=seed)
    predictions = model.predict(X_test, precision="float32")
    elapsed = time.perf_counter() - start
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "epochs": int(epochs),
        "learning_rate": float(alpha),
        "batch_size": int(batch_size),
        "seed": int(seed),
        "test_accuracy_percent": round(float(np.mean(predictions == y_test) * 100.0), 4),
        "training_time_seconds": round(float(elapsed), 4),
        "peak_memory_mb": round(float(peak_bytes / (1024 * 1024)), 4),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": dataset_name,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect training/test performance metrics.")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.1)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("metrics.json"))
    parser.add_argument(
        "--min-acceptable-accuracy",
        type=float,
        default=80.0,
        help="Minimum acceptable test accuracy percentage before failing the run.",
    )
    parser.add_argument("--no-synthetic-fallback", action="store_true", help="Disable synthetic fallback data")
    args = parser.parse_args()

    if args.epochs <= 0 or args.batch_size <= 0:
        raise ValueError("--epochs and --batch-size must be > 0")

    if args.min_acceptable_accuracy < 0.0 or args.min_acceptable_accuracy > 100.0:
        raise ValueError("--min-acceptable-accuracy must be between 0 and 100")

    metrics = collect_metrics(args.epochs, args.alpha, args.batch_size, args.seed, not args.no_synthetic_fallback)
    accuracy = float(metrics.get("test_accuracy_percent", 0.0))
    is_bad_metrics = accuracy < float(args.min_acceptable_accuracy)
    if is_bad_metrics:
        metrics["bad_metrics"] = True
        metrics["minimum_acceptable_accuracy_percent"] = float(args.min_acceptable_accuracy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    if is_bad_metrics:
        print(
            "[collect_metrics] WARNING: accuracy "
            f"{accuracy:.4f}% is below minimum acceptable threshold "
            f"{args.min_acceptable_accuracy:.4f}%. Marking metrics as bad and failing the run."
        )
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[collect_metrics] ERROR: {exc}")
        raise
