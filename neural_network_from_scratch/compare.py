"""Framework comparison between scratch NumPy model and PyTorch model."""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np

from neural_network_from_scratch.benchmark import (
    _measure_peak_memory_mb,
    make_synthetic_data,
    measure_batch_throughput,
    measure_inference_latency_per_sample,
    measure_training_time_per_epoch,
)
from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.pytorch_model import TorchNeuralNetwork, is_torch_available
from neural_network_from_scratch.reproducibility import set_global_seed
from neural_network_from_scratch.student import NeuralNetwork


def _repo_root():
    return Path(__file__).resolve().parents[2]


def _measure_torch_inference_latency_per_sample(model, X, precision="float32", runs=5):
    model.forward(X, training=False, precision=precision)
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        model.forward(X, training=False, precision=precision)
        times.append(time.perf_counter() - t0)
    return float(np.mean(times)) / X.shape[0]


def _measure_torch_throughput(model, X, precision="float32", runs=5):
    model.forward(X, training=False, precision=precision)
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        model.forward(X, training=False, precision=precision)
        times.append(time.perf_counter() - t0)
    avg_time = float(np.mean(times))
    return X.shape[0] / avg_time if avg_time > 0 else float("inf")


def _train_torch(model, X, y, epochs, alpha, batch_size, seed):
    t0 = time.perf_counter()
    history = model.fit(X, y, epochs=epochs, alpha=alpha, batch_size=batch_size, shuffle=True, seed=seed)
    elapsed = time.perf_counter() - t0
    return history, elapsed / epochs


def benchmark_scratch_vs_torch(
    layer_sizes,
    activations,
    n_samples=512,
    epochs=3,
    batch_size=32,
    alpha=0.1,
    seed=42,
):
    set_global_seed(seed)
    X, y = make_synthetic_data(n_samples=n_samples, n_features=layer_sizes[0], n_classes=layer_sizes[-1], seed=seed)

    cfg = PrecisionConfig(train_dtype="float32", infer_precision="float32", seed=seed)
    scratch = NeuralNetwork(layer_sizes=layer_sizes, activations=activations, precision_config=cfg)

    (scratch_pack, scratch_mem) = _measure_peak_memory_mb(
        measure_training_time_per_epoch, scratch, X, y, epochs, alpha, batch_size, seed
    )
    scratch_history, scratch_time = scratch_pack
    scratch_latency = measure_inference_latency_per_sample(scratch, X, precision="float32")
    scratch_throughput = measure_batch_throughput(scratch, X, precision="float32")

    rows: List[Dict[str, object]] = [
        {
            "framework": "scratch_numpy",
            "status": "ok",
            "seed": seed,
            "layer_sizes": "x".join(str(v) for v in layer_sizes),
            "epochs": epochs,
            "batch_size": batch_size,
            "alpha": alpha,
            "n_samples": n_samples,
            "train_time_per_epoch_s": round(scratch_time, 6),
            "inference_latency_per_sample_s": round(scratch_latency, 8),
            "batch_throughput_samples_per_s": round(scratch_throughput, 3),
            "peak_memory_mb": round(scratch_mem, 6),
            "final_accuracy": round(float(scratch_history["accuracy"][-1]), 6),
            "notes": "",
        }
    ]

    if not is_torch_available():
        rows.append(
            {
                "framework": "pytorch",
                "status": "skipped",
                "seed": seed,
                "layer_sizes": "x".join(str(v) for v in layer_sizes),
                "epochs": epochs,
                "batch_size": batch_size,
                "alpha": alpha,
                "n_samples": n_samples,
                "train_time_per_epoch_s": None,
                "inference_latency_per_sample_s": None,
                "batch_throughput_samples_per_s": None,
                "peak_memory_mb": None,
                "final_accuracy": None,
                "notes": "torch not installed",
            }
        )
        return rows

    torch_model = TorchNeuralNetwork(layer_sizes=layer_sizes, activations=activations, seed=seed)
    (torch_pack, torch_mem) = _measure_peak_memory_mb(
        lambda: _train_torch(torch_model, X, y, epochs, alpha, batch_size, seed)
    )
    torch_history, torch_time = torch_pack
    torch_latency = _measure_torch_inference_latency_per_sample(torch_model, X, precision="float32")
    torch_throughput = _measure_torch_throughput(torch_model, X, precision="float32")

    rows.append(
        {
            "framework": "pytorch",
            "status": "ok",
            "seed": seed,
            "layer_sizes": "x".join(str(v) for v in layer_sizes),
            "epochs": epochs,
            "batch_size": batch_size,
            "alpha": alpha,
            "n_samples": n_samples,
            "train_time_per_epoch_s": round(torch_time, 6),
            "inference_latency_per_sample_s": round(torch_latency, 8),
            "batch_throughput_samples_per_s": round(torch_throughput, 3),
            "peak_memory_mb": round(torch_mem, 6),
            "final_accuracy": round(float(torch_history["accuracy"][-1]), 6),
            "notes": "",
        }
    )
    return rows


def _save_csv(results, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "comparison_metrics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    return csv_path


def _save_json(results, out_dir: Path):
    json_path = out_dir / "comparison_metrics.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return json_path


def _save_plot(results, out_dir: Path):
    valid = [row for row in results if row["status"] == "ok"]
    if not valid:
        return None

    frameworks = [row["framework"] for row in valid]
    metrics = [
        ("train_time_per_epoch_s", "Train Time/Epoch (s)"),
        ("inference_latency_per_sample_s", "Inference Latency/Sample (s)"),
        ("peak_memory_mb", "Peak Memory (MB)"),
        ("final_accuracy", "Final Accuracy"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for ax, (metric_key, title) in zip(axes, metrics):
        vals = [row[metric_key] for row in valid]
        ax.bar(frameworks, vals, color=["#1f77b4", "#ff7f0e"][: len(valid)])
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=15)

    plt.tight_layout()
    plot_path = out_dir / "comparison_summary.png"
    plt.savefig(plot_path, dpi=150)
    plt.close(fig)
    return plot_path


def _print_table(results):
    columns = [
        "framework",
        "status",
        "train_time_per_epoch_s",
        "inference_latency_per_sample_s",
        "peak_memory_mb",
        "final_accuracy",
        "notes",
    ]
    header = " | ".join(f"{c:>30}" for c in columns)
    print(header)
    print("-" * len(header))
    for row in results:
        print(" | ".join(f"{str(row[c]):>30}" for c in columns))


def run_comparison():
    results = benchmark_scratch_vs_torch(
        layer_sizes=[32, 64, 4],
        activations=["relu", "softmax"],
        n_samples=256,
        epochs=3,
        batch_size=32,
        alpha=0.1,
        seed=42,
    )

    out_dir = _repo_root() / "benchmarks" / "comparison"
    csv_path = _save_csv(results, out_dir)
    json_path = _save_json(results, out_dir)
    plot_path = _save_plot(results, out_dir)

    _print_table(results)
    print(f"\nSaved CSV: {csv_path}")
    print(f"Saved JSON: {json_path}")
    print(f"Saved plot: {plot_path if plot_path else 'skipped (no valid comparison rows)'}")


if __name__ == "__main__":
    run_comparison()
