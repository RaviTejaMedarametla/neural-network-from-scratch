#!/usr/bin/env python3
"""Generate per-run benchmark report from metrics.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from neural_network_from_scratch.metrics_schema import normalize_metrics_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate benchmark report markdown from metrics.json")
    parser.add_argument("--metrics", type=Path, default=Path("metrics.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/metrics_report.md"))
    args = parser.parse_args()

    if not args.metrics.exists():
        raise FileNotFoundError(f"Metrics file not found: {args.metrics}")

    metrics = normalize_metrics_payload(json.loads(args.metrics.read_text(encoding="utf-8")))

    lines = [
        "# Benchmark Report",
        "",
        "Source: automated run using `scripts/collect_metrics.py`.",
        "",
        "## Raw Metrics",
        "",
        "```json",
        json.dumps(metrics, indent=2),
        "```",
        "",
        "## Summary",
        "",
        f"- Dataset: {metrics.get('dataset', 'N/A')}",
        f"- Accuracy (%): {metrics.get('test_accuracy_percent', 'N/A')}",
        f"- Training time (s): {metrics.get('training_time_seconds', 'N/A')}",
        f"- Peak memory (MB): {metrics.get('peak_memory_mb', 'N/A')}",
        f"- bad_metrics: {metrics.get('bad_metrics', 'N/A')}",
        f"- CPU count: {metrics.get('hardware_context', {}).get('cpu_count', 'N/A')}",
        f"- Resolved batch size: {metrics.get('hardware_context', {}).get('resolved_batch_size', metrics.get('batch_size', 'N/A'))}",
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
