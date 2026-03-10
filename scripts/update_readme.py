#!/usr/bin/env python3
"""Update README performance metrics section from metrics.json."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

METRICS_START = "<!-- METRICS_START -->"
METRICS_END = "<!-- METRICS_END -->"


def _format_timestamp(metrics: Dict[str, Any]) -> str:
    ts = metrics.get("generated_at_utc")
    if isinstance(ts, str) and ts:
        return ts
    return datetime.now(timezone.utc).isoformat()


def render_metrics_block(metrics: Dict[str, Any]) -> str:
    """Render markdown block inserted between metrics markers."""
    accuracy = metrics.get("test_accuracy_percent", "N/A")
    train_time = metrics.get("training_time_seconds", "N/A")
    peak_memory = metrics.get("peak_memory_mb", "N/A")
    epochs = metrics.get("epochs", "N/A")
    dataset = metrics.get("dataset", "unknown")
    generated_at = _format_timestamp(metrics)
    warning = metrics.get("warning")

    warning_line = f"\n> ⚠️ {warning}\n" if warning else ""

    return (
        "## Performance Metrics\n\n"
        "Latest automated benchmark run:\n\n"
        "| Metric | Value |\n"
        "|---|---:|\n"
        f"| Final test accuracy (%) | {accuracy} |\n"
        f"| Total training time (seconds) | {train_time} |\n"
        f"| Peak memory usage (MB) | {peak_memory} |\n"
        f"| Epochs | {epochs} |\n"
        f"| Dataset | {dataset} |\n"
        f"{warning_line}\n"
        f"_Last updated: {generated_at}_\n"
    )


def update_readme(readme_path: Path, metrics_path: Path) -> None:
    """Inject (or create) the metrics section in README using markers."""
    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {metrics_path}")
    if not readme_path.exists():
        raise FileNotFoundError(f"README file not found: {readme_path}")

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    rendered = render_metrics_block(metrics)
    readme = readme_path.read_text(encoding="utf-8")

    if METRICS_START in readme and METRICS_END in readme:
        start_idx = readme.index(METRICS_START)
        end_idx = readme.index(METRICS_END) + len(METRICS_END)
        replacement = f"{METRICS_START}\n{rendered}\n{METRICS_END}"
        updated = readme[:start_idx] + replacement + readme[end_idx:]
    else:
        block = f"\n\n{METRICS_START}\n{rendered}\n{METRICS_END}\n"
        updated = readme.rstrip() + block

    if not updated.endswith("\n"):
        updated += "\n"
    readme_path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update README metrics section from JSON.")
    parser.add_argument("--metrics", type=Path, default=Path("metrics.json"), help="Path to metrics.json")
    parser.add_argument("--readme", type=Path, default=Path("README.md"), help="Path to README.md")
    args = parser.parse_args()

    update_readme(readme_path=args.readme, metrics_path=args.metrics)
    print(f"Updated {args.readme} using {args.metrics}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[update_readme] ERROR: {exc}")
        raise
