#!/usr/bin/env python3
"""Write a normalized failure metrics payload for CI fallbacks."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from neural_network_from_scratch.metrics_schema import normalize_metrics_payload


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_failure_payload(error: str, dataset: str = "unknown", seed: int = 42) -> dict:
    payload = {
        "generated_at_utc": _timestamp(),
        "epochs": 0,
        "batch_size": 0,
        "learning_rate": 0.0,
        "seed": int(seed),
        "dataset": dataset,
        "bad_metrics": True,
        "error": str(error),
        "test_accuracy_percent": 0.0,
        "training_time_seconds": 0.0,
        "peak_memory_mb": 0.0,
    }
    return normalize_metrics_payload(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a normalized failure metrics payload")
    parser.add_argument("--output", type=Path, default=Path("metrics.json"))
    parser.add_argument("--error", type=str, required=True)
    parser.add_argument("--dataset", type=str, default="unknown")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    payload = build_failure_payload(error=args.error, dataset=args.dataset, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"[write_failure_metrics] wrote fallback payload to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
