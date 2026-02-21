"""Training entrypoint with experiment tracking and dataset integrity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import numpy as np

from config import EXPERIMENT_CONFIGS, PrecisionConfig
from dataset_config import DatasetSpec, FASHION_MNIST_SPEC, ensure_dataset_ready, file_digest, load_dataset
from experiment_manager import ExperimentManager
from reproducibility import get_rng, set_global_seed
from student import NeuralNetwork


def _resolve_experiment_config(config_name: str) -> Dict[str, Any]:
    if config_name in EXPERIMENT_CONFIGS:
        return dict(EXPERIMENT_CONFIGS[config_name])

    maybe_path = Path(config_name)
    if maybe_path.exists():
        return json.loads(maybe_path.read_text(encoding="utf-8"))

    raise ValueError(f"Unknown experiment config: {config_name}")


def _load_training_data(cfg: Dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    synthetic_mode = bool(cfg.get("synthetic_mode", False))

    if synthetic_mode:
        rng = get_rng(int(cfg.get("seed", 42)))
        n_samples = int(cfg.get("synthetic_samples", 512))
        n_features = int(cfg["layer_sizes"][0])
        n_classes = int(cfg["layer_sizes"][-1])
        X = rng.normal(size=(n_samples, n_features)).astype(np.float32)
        y = rng.integers(0, n_classes, size=n_samples, dtype=np.int32)
        print(f"[dataset] synthetic_mode=True, generated {n_samples} samples")
        return X, y

    dataset_path = cfg.get("dataset_path", FASHION_MNIST_SPEC.train_path)
    test_path = cfg.get("dataset_test_path", FASHION_MNIST_SPEC.test_path)
    dataset_spec = DatasetSpec(
        name=FASHION_MNIST_SPEC.name,
        version=cfg.get("dataset_version", FASHION_MNIST_SPEC.version),
        train_path=dataset_path,
        test_path=test_path,
    )
    ensure_dataset_ready(
        spec=dataset_spec,
        expected_features=int(cfg["layer_sizes"][0]),
        expected_min_rows=int(cfg.get("dataset_min_rows", 100)),
        auto_download=bool(cfg.get("dataset_auto_prepare", False)),
        expected_sha256=cfg.get("dataset_sha256"),
    )
    print(f"[dataset] loading {dataset_path}")
    return load_dataset(dataset_path)


def _train_val_split(X: np.ndarray, y: np.ndarray, val_ratio: float = 0.1, seed: int = 42):
    rng = get_rng(seed)
    idx = np.arange(X.shape[0])
    rng.shuffle(idx)

    val_size = max(1, int(len(idx) * val_ratio))
    val_idx = idx[:val_size]
    train_idx = idx[val_size:]

    return X[train_idx], y[train_idx], X[val_idx], y[val_idx]


def run_experiment(config_name: str):
    cfg = _resolve_experiment_config(config_name)
    seed = int(cfg.get("seed", 42))
    set_global_seed(seed)

    precision_cfg = PrecisionConfig(
        train_dtype=cfg.get("precision", "float32"),
        infer_precision=cfg.get("precision", "float32"),
        seed=seed,
    )

    model = NeuralNetwork(
        layer_sizes=cfg["layer_sizes"],
        activations=cfg["activations"],
        precision_config=precision_cfg,
    )

    X, y = _load_training_data(cfg)
    X_train, y_train, X_val, y_val = _train_val_split(
        X,
        y,
        val_ratio=float(cfg.get("val_ratio", 0.1)),
        seed=seed,
    )

    manager = ExperimentManager(log_dir="experiments/logs")

    metadata = {
        "precision": cfg.get("precision", "float32"),
        "model_size": "x".join(str(v) for v in cfg["layer_sizes"]),
        "dataset_version": cfg.get("dataset_version", FASHION_MNIST_SPEC.version),
        "dataset_sha256": None if cfg.get("synthetic_mode", False) else file_digest(cfg.get("dataset_path", FASHION_MNIST_SPEC.train_path)),
        "hardware_constraint_mode": cfg.get("hardware_constraint_mode", "off"),
        "synthetic_mode": bool(cfg.get("synthetic_mode", False)),
    }
    hyperparameters = {
        "epochs": int(cfg.get("epochs", 3)),
        "alpha": float(cfg.get("alpha", 0.1)),
        "batch_size": int(cfg.get("batch_size", 32)),
        "seed": seed,
        "activations": cfg.get("activations"),
        "layer_sizes": cfg.get("layer_sizes"),
    }

    record = manager.start_experiment(config_name=config_name, hyperparameters=hyperparameters, metadata=metadata)

    history = model.fit(
        X_train,
        y_train,
        epochs=hyperparameters["epochs"],
        alpha=hyperparameters["alpha"],
        batch_size=hyperparameters["batch_size"],
        seed=hyperparameters["seed"],
        X_val=X_val,
        y_val=y_val,
    )

    manager.log_metrics(history)

    checkpoint_dir = Path("experiments") / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = checkpoint_dir / f"{record.experiment_id}_v{record.version}.npz"
    model.save_weights(str(checkpoint_path))
    manager.add_checkpoint(str(checkpoint_path))

    print(f"Experiment logged: {record.experiment_id} v{record.version}")
    print(f"History file: experiments/logs/{record.experiment_id}.json")
    print(f"Checkpoint: {checkpoint_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run model training with experiment tracking.")
    parser.add_argument("--experiment", required=True, help="Experiment config name or JSON config path")
    args = parser.parse_args()
    run_experiment(args.experiment)
