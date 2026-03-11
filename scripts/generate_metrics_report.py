#!/usr/bin/env python3
"""Generate per-run benchmark report from metrics.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from neural_network_from_scratch.metrics_schema import KEY_ACCURACY, KEY_PEAK_MEMORY_MB, get_dataset_source, get_training_time_seconds


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate benchmark report markdown from metrics.json")
    parser.add_argument("--metrics", type=Path, default=Path("metrics.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/metrics_report.md"))
    args = parser.parse_args()

    if not args.metrics.exists():
        raise FileNotFoundError(f"Metrics file not found: {args.metrics}")

    metrics = json.loads(args.metrics.read_text(encoding="utf-8"))

    accuracy = metrics.get(KEY_ACCURACY, "N/A")
    train_time = get_training_time_seconds(metrics, "N/A")
    peak_memory = metrics.get(KEY_PEAK_MEMORY_MB, "N/A")
    dataset = get_dataset_source(metrics, "N/A")

    lines = [
        "# Benchmark Report",
        "",
        "Source: automated run using `scripts/collect_metrics.py`.",
        "",
        "## Summary",
        "",
        f"- Dataset: {dataset}",
        f"- Accuracy (%): {accuracy}",
        f"- Training time (s): {train_time}",
        f"- Peak memory (MB): {peak_memory}",
        "",
        "## Raw Metrics",
        "",
        "```json",
        json.dumps(metrics, indent=2),
        "```",
        "",
        "## Desired Baseline (MNIST/Fashion-MNIST, 5 epochs)",
        "",
        "| Metric | Desired Range | Notes |",
        "|---|---:|---|",
        "| Accuracy | 92–97% | Simple MLP can hit ~95% in 5 epochs |",
        "| Training time | 30–120 sec | Depends on CPU, batch size |",
        "| Memory usage | 100–500 MB | Depends on model size |",
        "",
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
