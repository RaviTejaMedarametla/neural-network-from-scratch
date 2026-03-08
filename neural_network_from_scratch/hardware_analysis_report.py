"""Build hardware-oriented analysis tables from benchmark and profiling outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

BYTES_PER_DTYPE = {"float32": 4, "float16": 2, "int8": 1}


def _load_profile(profile_path: Path) -> dict:
    return json.loads(profile_path.read_text(encoding="utf-8"))


def build_layer_table(profile: dict, batch_size: int) -> pd.DataFrame:
    rows = []
    for layer in profile.get("layer_wise_parameters", []):
        layer_total = int(layer.get("total", 0))
        bytes_f32 = layer_total * BYTES_PER_DTYPE["float32"]
        rows.append(
            {
                "layer": layer.get("layer"),
                "type": layer.get("type"),
                "parameters": layer_total,
                "parameter_memory_kb_f32": round(bytes_f32 / 1024, 3),
                "batch_size": int(batch_size),
            }
        )
    return pd.DataFrame(rows)


def build_precision_table(benchmark_df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        benchmark_df.groupby("precision_mode", as_index=False)
        .agg(
            latency_s=("inference_latency_per_sample_s", "mean"),
            throughput_samples_s=("batch_throughput_samples_per_s", "mean"),
            peak_memory_mb=("peak_memory_mb", "mean"),
            cpu_utilization_percent=("cpu_utilization_percent", "mean"),
        )
        .sort_values("latency_s")
    )

    grouped["effective_bandwidth_mb_s"] = (
        grouped["throughput_samples_s"] * grouped["peak_memory_mb"]
    ).round(3)
    grouped["notes"] = "Simulation-level estimate"
    return grouped


def write_reports(benchmark_csv: Path, profile_json: Path, output_dir: Path, batch_size: int) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    benchmark_df = pd.read_csv(benchmark_csv)
    profile = _load_profile(profile_json)

    layer_table = build_layer_table(profile, batch_size=batch_size)
    precision_table = build_precision_table(benchmark_df)

    layer_path = output_dir / "layer_memory_breakdown.csv"
    precision_path = output_dir / "precision_tradeoff_table.csv"
    layer_table.to_csv(layer_path, index=False)
    precision_table.to_csv(precision_path, index=False)
    return layer_path, precision_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate hardware analysis tables from existing artifacts")
    parser.add_argument("--benchmark-csv", default="benchmarks/benchmark_results.csv")
    parser.add_argument("--profile-json", default="profiling/profile_neuralnetwork.json")
    parser.add_argument("--output-dir", default="hardware_results")
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    layer_path, precision_path = write_reports(
        benchmark_csv=Path(args.benchmark_csv),
        profile_json=Path(args.profile_json),
        output_dir=Path(args.output_dir),
        batch_size=args.batch_size,
    )
    print(f"Saved layer table: {layer_path}")
    print(f"Saved precision table: {precision_path}")


if __name__ == "__main__":
    main()
