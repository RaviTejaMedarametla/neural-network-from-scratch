import argparse
import csv
import json
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np

from benchmark import make_synthetic_data, measure_inference_latency_per_sample, measure_batch_throughput
from config import PrecisionConfig
from runtime_model import NeuralNetwork
from reproducibility import set_global_seed
from energy_estimation import estimate_runtime_energy_j


@dataclass
class ScalingConfig:
    dataset_sizes: List[int]
    model_depths: List[int]
    precision_modes: List[str]
    input_dim: int = 32
    hidden_dim: int = 64
    n_classes: int = 4
    epochs: int = 2
    alpha: float = 0.1
    batch_size: int = 32
    seed: int = 42
    hardware_profile: str = "baseline_cpu"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _build_layer_sizes(input_dim: int, hidden_dim: int, n_classes: int, depth: int) -> List[int]:
    if depth < 1:
        raise ValueError("depth must be >= 1")
    return [input_dim] + [hidden_dim] * depth + [n_classes]


def _build_activations(depth: int) -> List[str]:
    return ["relu"] * depth + ["softmax"]


def _train_with_peak_memory(model, X, y, epochs, alpha, batch_size, seed):
    tracemalloc.start()
    t0 = time.perf_counter()
    try:
        history = model.fit(X, y, epochs=epochs, alpha=alpha, batch_size=batch_size, shuffle=True, seed=seed)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    elapsed = time.perf_counter() - t0
    return history, elapsed, peak / (1024 * 1024)


def run_scaling_study(config: ScalingConfig, output_dir: Path | None = None) -> List[Dict[str, float]]:
    destination = output_dir or (_repo_root() / "experiments" / "scaling")
    set_global_seed(config.seed)
    destination.mkdir(parents=True, exist_ok=True)

    rows = []
    for n_samples in config.dataset_sizes:
        for depth in config.model_depths:
            layer_sizes = _build_layer_sizes(config.input_dim, config.hidden_dim, config.n_classes, depth)
            activations = _build_activations(depth)
            X, y = make_synthetic_data(n_samples, config.input_dim, config.n_classes, seed=config.seed)

            for precision_mode in config.precision_modes:
                precision_cfg = PrecisionConfig(
                    train_dtype="float32",
                    infer_precision=precision_mode,
                    seed=config.seed,
                )
                model = NeuralNetwork(layer_sizes=layer_sizes, activations=activations, precision_config=precision_cfg)
                history, train_elapsed, peak_mem_mb = _train_with_peak_memory(
                    model=model,
                    X=X,
                    y=y,
                    epochs=config.epochs,
                    alpha=config.alpha,
                    batch_size=config.batch_size,
                    seed=config.seed,
                )

                latency = measure_inference_latency_per_sample(model, X, precision=precision_mode, runs=3)
                throughput = measure_batch_throughput(model, X, precision=precision_mode, runs=3)
                y_pred = model.predict(X, precision=precision_mode)
                accuracy = float(np.mean(y_pred == y))
                energy_j = estimate_runtime_energy_j(train_elapsed, precision_mode=precision_mode)

                rows.append(
                    {
                        "dataset_size": n_samples,
                        "model_depth": depth,
                        "precision_mode": precision_mode,
                        "train_time_s": round(train_elapsed, 6),
                        "inference_latency_s": round(latency, 8),
                        "peak_memory_mb": round(peak_mem_mb, 6),
                        "accuracy": round(accuracy, 6),
                        "throughput_samples_per_s": round(throughput, 3),
                        "energy_j": round(energy_j, 6),
                        "epochs": config.epochs,
                        "batch_size": config.batch_size,
                        "hardware_profile": config.hardware_profile,
                    }
                )

    _save_csv(rows, destination / "scaling_results.csv")
    _save_json(rows, destination / "scaling_results.json")
    _save_summary(rows, destination / "summary_report.md", config)
    _save_plots(rows, destination)
    return rows


def _save_csv(rows: List[Dict[str, float]], path: Path) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _save_json(rows: List[Dict[str, float]], path: Path) -> None:
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def _aggregate(rows: List[Dict[str, float]], x_key: str, y_key: str) -> Dict[int, float]:
    grouped: Dict[int, List[float]] = {}
    for row in rows:
        grouped.setdefault(int(row[x_key]), []).append(float(row[y_key]))
    return {k: float(np.mean(v)) for k, v in sorted(grouped.items())}


def _save_plots(rows: List[Dict[str, float]], out_dir: Path) -> None:
    metrics = [
        ("train_time_s", "training_time_curve.png", "Training Time (s)"),
        ("inference_latency_s", "inference_latency_curve.png", "Inference Latency (s)"),
        ("peak_memory_mb", "memory_usage_curve.png", "Peak Memory (MB)"),
        ("accuracy", "accuracy_curve.png", "Accuracy"),
        ("throughput_samples_per_s", "throughput_curve.png", "Throughput (samples/s)"),
        ("energy_j", "energy_curve.png", "Estimated Energy (J)"),
    ]

    for metric_key, filename, ylabel in metrics:
        agg = _aggregate(rows, "dataset_size", metric_key)
        x = list(agg.keys())
        y = list(agg.values())

        plt.figure(figsize=(7, 4))
        plt.plot(x, y, marker="o")
        plt.title(f"Scaling Curve: {ylabel} vs Dataset Size")
        plt.xlabel("Dataset Size")
        plt.ylabel(ylabel)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(out_dir / filename, dpi=140)
        plt.close()


def _save_summary(rows: List[Dict[str, float]], summary_path: Path, config: ScalingConfig) -> None:
    if not rows:
        summary_path.write_text("No results generated.\n", encoding="utf-8")
        return

    best_accuracy = max(rows, key=lambda r: r["accuracy"])
    fastest_train = min(rows, key=lambda r: r["train_time_s"])
    lowest_memory = min(rows, key=lambda r: r["peak_memory_mb"])
    lowest_energy = min(rows, key=lambda r: r["energy_j"])

    summary = [
        "# Scalability and Efficiency Study Summary",
        "",
        f"- Total experiment runs: {len(rows)}",
        f"- Dataset sizes: {config.dataset_sizes}",
        f"- Model depths: {config.model_depths}",
        f"- Precision modes: {config.precision_modes}",
        f"- Hardware profile tag: {config.hardware_profile}",
        "",
        "## Highlights",
        f"- Best accuracy: {best_accuracy['accuracy']} at dataset={best_accuracy['dataset_size']}, depth={best_accuracy['model_depth']}, precision={best_accuracy['precision_mode']}",
        f"- Fastest training: {fastest_train['train_time_s']}s at dataset={fastest_train['dataset_size']}, depth={fastest_train['model_depth']}, precision={fastest_train['precision_mode']}",
        f"- Lowest memory: {lowest_memory['peak_memory_mb']}MB at dataset={lowest_memory['dataset_size']}, depth={lowest_memory['model_depth']}, precision={lowest_memory['precision_mode']}",
        f"- Lowest estimated energy: {lowest_energy['energy_j']}J at dataset={lowest_energy['dataset_size']}, depth={lowest_energy['model_depth']}, precision={lowest_energy['precision_mode']}",
    ]

    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")


def default_scaling_config() -> ScalingConfig:
    return ScalingConfig(
        dataset_sizes=[128, 512, 1024],
        model_depths=[1, 2, 3],
        precision_modes=["float32", "float16", "int8"],
    )


def main():
    parser = argparse.ArgumentParser(description="Run scalability and efficiency study.")
    parser.add_argument("--quick", action="store_true", help="Run a smaller quick grid")
    args = parser.parse_args()

    if args.quick:
        config = ScalingConfig(
            dataset_sizes=[64, 128],
            model_depths=[1, 2],
            precision_modes=["float32", "float16"],
            epochs=1,
        )
    else:
        config = default_scaling_config()

    rows = run_scaling_study(config)
    print(f"Generated {len(rows)} runs in experiments/scaling")


if __name__ == "__main__":
    main()
