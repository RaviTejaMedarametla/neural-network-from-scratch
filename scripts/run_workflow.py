"""Standardized CLI for reproducible experiment workflows."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = REPO_ROOT / "Neural Network from Scratch" / "task"


def run_step(command: list[str]) -> None:
    print(f"[workflow] {' '.join(command)}")
    subprocess.run(command, check=True, cwd=REPO_ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run standardized experiment workflows")
    parser.add_argument(
        "--mode",
        choices=["train", "benchmark", "full"],
        default="full",
        help="Workflow mode to execute",
    )
    parser.add_argument(
        "--experiment",
        default="baseline",
        help="Experiment config name or JSON path for training mode",
    )
    parser.add_argument(
        "--stats-repeats",
        type=int,
        default=5,
        help="Repeats for statistical analysis",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Global seed forwarded to benchmark and statistical analysis steps",
    )
    args = parser.parse_args()

    python = sys.executable
    train_cmd = [python, str(TASK_DIR / "train.py"), "--experiment", args.experiment]
    benchmark_cmd = [python, str(TASK_DIR / "benchmark.py"), "--seed", str(args.seed)]
    stats_cmd = [
        python,
        str(TASK_DIR / "statistical_analysis.py"),
        "--repeats",
        str(args.stats_repeats),
        "--seed",
        str(args.seed),
    ]

    if args.mode == "train":
        run_step(train_cmd)
        return

    if args.mode == "benchmark":
        run_step(benchmark_cmd)
        run_step(stats_cmd)
        return

    run_step(train_cmd)
    run_step(benchmark_cmd)
    run_step(stats_cmd)


if __name__ == "__main__":
    main()
