"""Stress testing under constrained memory and precision modes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.hardware_simulation import config_from_precision_config, run_training_with_hardware_constraints
from neural_network_from_scratch.reproducibility import set_global_seed
from neural_network_from_scratch.student import NeuralNetwork


def run_stress(output_path: Path) -> None:
    set_global_seed(42)
    X = np.random.default_rng(42).normal(size=(512, 32)).astype(np.float32)
    y = np.random.default_rng(43).integers(0, 4, size=512, dtype=np.int32)

    scenarios = []
    for precision in ["float32", "float16", "int8"]:
        for max_mem in [0.02, 0.05, 0.1, 0.5, 2.0]:
            for batch_limit in [32, 64, 128]:
                cfg = PrecisionConfig(
                    seed=42,
                    enable_hardware_simulation=True,
                    precision_mode=precision,
                    max_memory_mb=max_mem,
                    batch_size_limit=batch_limit,
                    compute_speed_factor=1.25 if precision != "int8" else 1.5,
                )
                model = NeuralNetwork([32, 64, 4], ["relu", "softmax"], precision_config=cfg)
                sim_cfg = config_from_precision_config(cfg)
                result = run_training_with_hardware_constraints(
                    model,
                    X,
                    y,
                    epochs=1,
                    alpha=0.1,
                    batch_size=128,
                    seed=42,
                    simulation_config=sim_cfg,
                )
                scenarios.append(
                    {
                        "precision": precision,
                        "max_memory_mb": max_mem,
                        "batch_size_limit": batch_limit,
                        "effective_batch": result["setup"]["batch_size"],
                        "estimated_memory_mb": result["setup"].get("estimated_memory_mb"),
                        "warning_count": len(result["setup"]["warnings"]),
                        "effective_time_s": result["effective_time_s"],
                        "accuracy": result["final_accuracy"],
                    }
                )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(scenarios[0].keys()))
        writer.writeheader()
        writer.writerows(scenarios)
    print(f"Saved stress test results to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run memory-constrained stress tests")
    parser.add_argument("--output", default="experiments/scaling/hardware_stress.csv")
    args = parser.parse_args()
    run_stress(Path(args.output))


if __name__ == "__main__":
    main()
