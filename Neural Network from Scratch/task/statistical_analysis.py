"""Statistical benchmarking utilities with confidence intervals and Pareto plots."""

from __future__ import annotations

import argparse
import csv
import json
from math import sqrt
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np

from benchmark import benchmark_one_setup
from reproducibility import set_global_seed


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _ci95(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    return 1.96 * (stdev(values) / sqrt(len(values)))


def run_repeated_benchmarks(
    layer_sizes: List[int],
    activations: List[str],
    precision_modes: List[str],
    batch_size: int,
    n_samples: int,
    epochs: int,
    repeats: int,
    seed: int,
    output_dir: Path | None = None,
) -> List[Dict[str, float]]:
    set_global_seed(seed)
    out_dir = output_dir or (_repo_root() / "benchmarks" / "statistical")
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_rows = []
    for precision_mode in precision_modes:
        for r in range(repeats):
            run_seed = seed + r
            result = benchmark_one_setup(
                layer_sizes=layer_sizes,
                activations=activations,
                precision_mode=precision_mode,
                batch_size=batch_size,
                n_samples=n_samples,
                epochs=epochs,
                seed=run_seed,
            )
            result["repeat_id"] = r
            raw_rows.append(result)

    summary_rows: List[Dict[str, float]] = []
    for precision_mode in precision_modes:
        selected = [row for row in raw_rows if row["precision_mode"] == precision_mode]

        def aggregate(metric: str):
            vals = [float(row[metric]) for row in selected]
            return mean(vals), (stdev(vals) if len(vals) > 1 else 0.0), _ci95(vals)

        train_mean, train_std, train_ci = aggregate("train_time_per_epoch_s")
        lat_mean, lat_std, lat_ci = aggregate("inference_latency_per_sample_s")
        mem_mean, mem_std, mem_ci = aggregate("peak_memory_mb")
        acc_mean, acc_std, acc_ci = aggregate("final_train_accuracy")
        energy_mean, energy_std, energy_ci = aggregate("energy_per_epoch_j")

        summary_rows.append(
            {
                "precision_mode": precision_mode,
                "repeats": repeats,
                "train_time_mean": round(train_mean, 6),
                "train_time_std": round(train_std, 6),
                "train_time_ci95": round(train_ci, 6),
                "latency_mean": round(lat_mean, 8),
                "latency_std": round(lat_std, 8),
                "latency_ci95": round(lat_ci, 8),
                "memory_mean": round(mem_mean, 6),
                "memory_std": round(mem_std, 6),
                "memory_ci95": round(mem_ci, 6),
                "accuracy_mean": round(acc_mean, 6),
                "accuracy_std": round(acc_std, 6),
                "accuracy_ci95": round(acc_ci, 6),
                "energy_mean": round(energy_mean, 6),
                "energy_std": round(energy_std, 6),
                "energy_ci95": round(energy_ci, 6),
            }
        )

    _save_csv(raw_rows, out_dir / "raw_runs.csv")
    _save_csv(summary_rows, out_dir / "summary_stats.csv")
    (out_dir / "summary_stats.json").write_text(json.dumps(summary_rows, indent=2), encoding="utf-8")
    _save_tradeoff_plots(summary_rows, out_dir)
    _save_pareto_plot(summary_rows, out_dir)
    return summary_rows


def _save_csv(rows: List[Dict[str, float]], path: Path) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _save_tradeoff_plots(summary_rows: List[Dict[str, float]], out_dir: Path) -> None:
    precisions = [r["precision_mode"] for r in summary_rows]
    acc = [r["accuracy_mean"] for r in summary_rows]
    lat = [r["latency_mean"] for r in summary_rows]
    mem = [r["memory_mean"] for r in summary_rows]
    energy = [r["energy_mean"] for r in summary_rows]

    plt.figure(figsize=(6, 4))
    plt.scatter(lat, acc)
    for p, x, y in zip(precisions, lat, acc):
        plt.annotate(p, (x, y))
    plt.xlabel("Latency (s/sample)")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Latency")
    plt.tight_layout()
    plt.savefig(out_dir / "accuracy_vs_latency.png", dpi=140)
    plt.close()


    plt.figure(figsize=(6, 4))
    plt.scatter(energy, acc)
    for p, x, y in zip(precisions, energy, acc):
        plt.annotate(p, (x, y))
    plt.xlabel("Estimated Energy per Epoch (J)")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Energy")
    plt.tight_layout()
    plt.savefig(out_dir / "accuracy_vs_energy.png", dpi=140)
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.scatter(mem, acc)
    for p, x, y in zip(precisions, mem, acc):
        plt.annotate(p, (x, y))
    plt.xlabel("Peak Memory (MB)")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Memory")
    plt.tight_layout()
    plt.savefig(out_dir / "accuracy_vs_memory.png", dpi=140)
    plt.close()


def _save_pareto_plot(summary_rows: List[Dict[str, float]], out_dir: Path) -> None:
    points = [(r["latency_mean"], r["accuracy_mean"], r["precision_mode"]) for r in summary_rows]

    pareto = []
    for i, (lat_i, acc_i, mode_i) in enumerate(points):
        dominated = False
        for j, (lat_j, acc_j, _) in enumerate(points):
            if i == j:
                continue
            if lat_j <= lat_i and acc_j >= acc_i and (lat_j < lat_i or acc_j > acc_i):
                dominated = True
                break
        if not dominated:
            pareto.append((lat_i, acc_i, mode_i))

    plt.figure(figsize=(6, 4))
    for lat, acc, mode in points:
        plt.scatter(lat, acc, color="gray")
        plt.annotate(mode, (lat, acc))

    if pareto:
        pareto_sorted = sorted(pareto, key=lambda x: x[0])
        xs = [p[0] for p in pareto_sorted]
        ys = [p[1] for p in pareto_sorted]
        plt.plot(xs, ys, color="red", linewidth=2, label="Pareto frontier")

    plt.xlabel("Latency (s/sample)")
    plt.ylabel("Accuracy")
    plt.title("Pareto Frontier (Accuracy vs Latency)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "pareto_frontier.png", dpi=140)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run statistical benchmarks with repeated runs")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows = run_repeated_benchmarks(
        layer_sizes=[32, 64, 4],
        activations=["relu", "softmax"],
        precision_modes=["float32", "float16", "int8"],
        batch_size=32,
        n_samples=256,
        epochs=2,
        repeats=args.repeats,
        seed=args.seed,
    )
    print(f"Saved statistical benchmark artifacts for {len(rows)} precision modes")


if __name__ == "__main__":
    main()
