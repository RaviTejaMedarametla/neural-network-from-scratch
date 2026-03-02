"""Generate aggregated benchmark reports from benchmark CSV outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def build_report(input_csv: Path, output_csv: Path) -> Path:
    df = pd.read_csv(input_csv)
    required = {
        "precision_mode",
        "batch_size",
        "train_time_per_epoch_s",
        "inference_latency_per_sample_s",
        "peak_memory_mb",
        "final_train_accuracy",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns for report generation: {sorted(missing)}")

    grouped = (
        df.groupby(["precision_mode", "batch_size"], as_index=False)
        .agg(
            runs=("seed", "count"),
            train_time_mean_s=("train_time_per_epoch_s", "mean"),
            train_time_std_s=("train_time_per_epoch_s", "std"),
            latency_mean_s=("inference_latency_per_sample_s", "mean"),
            latency_std_s=("inference_latency_per_sample_s", "std"),
            peak_memory_mean_mb=("peak_memory_mb", "mean"),
            peak_memory_std_mb=("peak_memory_mb", "std"),
            accuracy_mean=("final_train_accuracy", "mean"),
            accuracy_std=("final_train_accuracy", "std"),
        )
        .fillna(0.0)
        .sort_values(["precision_mode", "batch_size"])
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    grouped.to_csv(output_csv, index=False)
    return output_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate benchmark CSV into grouped summary metrics")
    parser.add_argument("--input", default="benchmarks/benchmark_results.csv")
    parser.add_argument("--output", default="benchmarks/benchmark_summary.csv")
    args = parser.parse_args()

    output_path = build_report(Path(args.input), Path(args.output))
    print(f"Saved benchmark summary: {output_path}")


if __name__ == "__main__":
    main()
