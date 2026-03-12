from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import ExperimentConfig
from .experiments import run_research_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run hardware-aware neural-network research experiment")
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--precision-bits", type=int, choices=[4, 8, 16, 32], default=8)
    parser.add_argument("--output", type=str, default="artifacts")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = ExperimentConfig()
    config.training.epochs = args.epochs
    config.training.batch_size = args.batch_size
    config.hardware.precision_bits = args.precision_bits

    result = run_research_experiment(config=config, output_dir=args.output)

    metrics = result.research_metrics
    print(json.dumps(metrics, indent=2))
    print(f"Results written to {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
