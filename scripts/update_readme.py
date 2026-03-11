#!/usr/bin/env python3
"""Update README performance metrics section from metrics.json.

Publishes only quality-gated metrics. On unreliable runs, shows a warning and retains
last known good metrics from a dedicated backup payload when available.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from neural_network_from_scratch.metrics_schema import (
    KEY_ACCURACY,
    KEY_BAD_METRICS,
    KEY_PEAK_MEMORY_MB,
    get_dataset_source,
    get_training_time_seconds,
)

METRICS_START = "<!-- METRICS_START -->"
METRICS_END = "<!-- METRICS_END -->"
WARNING_START = "<!-- METRICS_WARNING_START -->"
WARNING_END = "<!-- METRICS_WARNING_END -->"


def _num(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _format_timestamp(metrics: Dict[str, Any]) -> str:
    source_ts = metrics.get("generated_at_utc")
    if isinstance(source_ts, str) and source_ts.strip():
        return source_ts
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def render_metrics_block(metrics: Dict[str, Any]) -> str:
    generated_at = _format_timestamp(metrics)
    accuracy = metrics.get(KEY_ACCURACY, "N/A")
    train_time = get_training_time_seconds(metrics, "N/A")
    peak_memory = metrics.get(KEY_PEAK_MEMORY_MB, "N/A")
    epochs = metrics.get("epochs", "N/A")
    dataset = get_dataset_source(metrics, "N/A")

    return (
        "## Performance Metrics\n\n"
        "Latest automated benchmark run (published only if quality gates pass):\n\n"
        "| Metric | Value | Desired Range | Notes |\n"
        "|---|---:|---:|---|\n"
        f"| Final test accuracy (%) | {accuracy} | 92–97 | Simple MLP can hit ~95% in 5 epochs |\n"
        f"| Total training time (seconds) | {train_time} | 30–120 | Depends on CPU, batch size |\n"
        f"| Peak memory usage (MB) | {peak_memory} | 100–500 | Depends on model size |\n"
        f"| Epochs | {epochs} | 5 | Benchmark baseline |\n"
        f"| Dataset source | {dataset} | MNIST/Fashion-MNIST | Must not be synthetic fallback |\n\n"
        f"_Last metrics payload timestamp: {generated_at}_\n"
    )


def _default_metrics_placeholder() -> str:
    return (
        "## Performance Metrics\n\n"
        "Latest automated benchmark run (published only if quality gates pass):\n\n"
        "_No known good metrics are available yet._\n"
    )


def render_warning(reason: str, accuracy: Any, min_acceptable_accuracy: float) -> str:
    accuracy_value = _num(accuracy)
    accuracy_text = f"{accuracy_value:.4f}" if accuracy_value is not None else "N/A"
    return (
        f"{WARNING_START}\n"
        "⚠️ Warning: The latest automated benchmark produced unreliable results "
        f"(accuracy = {accuracy_text}%; minimum acceptable = {min_acceptable_accuracy:.2f}%). "
        "The model may need debugging. The last known good numbers are shown below. "
        f"Reason: {reason}.\n"
        f"{WARNING_END}\n"
    )


def _remove_existing_warning(readme: str) -> str:
    pattern = rf"\n?{re.escape(WARNING_START)}.*?{re.escape(WARNING_END)}\n?"
    return re.sub(pattern, "\n", readme, flags=re.DOTALL)


def _upsert_metrics_section(readme: str, block: str) -> str:
    replacement = f"{METRICS_START}\n{block}\n{METRICS_END}"
    if METRICS_START in readme and METRICS_END in readme:
        start_idx = readme.index(METRICS_START)
        end_idx = readme.index(METRICS_END) + len(METRICS_END)
        return readme[:start_idx] + replacement + readme[end_idx:]
    return readme.rstrip() + f"\n\n{replacement}\n"


def _load_json(path: Path) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    if not path.exists():
        return None, f"file not found: {path}"
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"could not parse {path}: {exc}"
    if not isinstance(loaded, dict):
        return None, f"{path} must contain a JSON object"
    return loaded, None


def _quality_gate(
    metrics: Dict[str, Any],
    min_acceptable_accuracy: float,
    publish_min_accuracy: float,
    publish_min_time: float,
    publish_max_time: float,
    publish_min_memory: float,
    publish_max_memory: float,
) -> tuple[bool, str]:
    if metrics.get(KEY_BAD_METRICS) is True:
        return False, "metrics.json explicitly flagged bad_metrics=true"

    dataset = get_dataset_source(metrics, "").strip().lower()
    if not dataset or "synthetic" in dataset:
        return False, "dataset source is synthetic/unknown"

    accuracy = _num(metrics.get(KEY_ACCURACY))
    train_time = _num(get_training_time_seconds(metrics))
    peak_memory = _num(metrics.get(KEY_PEAK_MEMORY_MB))

    if accuracy is None:
        return False, "accuracy missing or non-numeric"
    if train_time is None:
        return False, "training time missing or non-numeric"
    if peak_memory is None:
        return False, "peak memory missing or non-numeric"

    if accuracy < min_acceptable_accuracy:
        return False, "accuracy below minimum acceptable threshold"
    if accuracy < publish_min_accuracy:
        return False, f"accuracy {accuracy:.4f}% below publish threshold {publish_min_accuracy:.2f}%"
    if not (publish_min_time <= train_time <= publish_max_time):
        return False, f"training time {train_time:.4f}s outside publish range [{publish_min_time:.2f}, {publish_max_time:.2f}]s"
    if not (publish_min_memory <= peak_memory <= publish_max_memory):
        return False, f"peak memory {peak_memory:.4f}MB outside publish range [{publish_min_memory:.2f}, {publish_max_memory:.2f}]MB"

    return True, "passed"


def update_readme(
    readme_path: Path,
    metrics_path: Path,
    last_good_metrics_path: Path,
    min_acceptable_accuracy: float,
    publish_min_accuracy: float,
    publish_min_time: float,
    publish_max_time: float,
    publish_min_memory: float,
    publish_max_memory: float,
) -> None:
    if not readme_path.exists():
        raise FileNotFoundError(f"README file not found: {readme_path}")

    current_metrics, load_error = _load_json(metrics_path)
    readme = _remove_existing_warning(readme_path.read_text(encoding="utf-8"))

    publishable = False
    reason = load_error or "metrics.json unavailable"
    accuracy: Any = None

    if current_metrics is not None:
        publishable, reason = _quality_gate(
            current_metrics,
            min_acceptable_accuracy,
            publish_min_accuracy,
            publish_min_time,
            publish_max_time,
            publish_min_memory,
            publish_max_memory,
        )
        accuracy = current_metrics.get(KEY_ACCURACY)

    if publishable and current_metrics is not None:
        last_good_metrics_path.parent.mkdir(parents=True, exist_ok=True)
        last_good_metrics_path.write_text(json.dumps(current_metrics, indent=2) + "\n", encoding="utf-8")
        updated = _upsert_metrics_section(readme, render_metrics_block(current_metrics))
    else:
        last_good_metrics, _ = _load_json(last_good_metrics_path)
        preserved_block = render_metrics_block(last_good_metrics) if last_good_metrics else _default_metrics_placeholder()
        readme = _upsert_metrics_section(readme, preserved_block)
        warning = render_warning(reason=reason, accuracy=accuracy, min_acceptable_accuracy=min_acceptable_accuracy)
        insert_at = readme.index(METRICS_START)
        updated = readme[:insert_at] + warning + readme[insert_at:]

    readme_path.write_text(updated + ("\n" if not updated.endswith("\n") else ""), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update README metrics section from JSON.")
    parser.add_argument("--metrics", type=Path, default=Path("metrics.json"))
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--last-good-metrics", type=Path, default=Path("artifacts/last_good_metrics.json"))
    parser.add_argument("--min-acceptable-accuracy", type=float, default=80.0)
    parser.add_argument("--publish-min-accuracy", type=float, default=92.0)
    parser.add_argument("--publish-min-time", type=float, default=30.0)
    parser.add_argument("--publish-max-time", type=float, default=120.0)
    parser.add_argument("--publish-min-memory", type=float, default=100.0)
    parser.add_argument("--publish-max-memory", type=float, default=500.0)
    args = parser.parse_args()

    update_readme(
        readme_path=args.readme,
        metrics_path=args.metrics,
        last_good_metrics_path=args.last_good_metrics,
        min_acceptable_accuracy=args.min_acceptable_accuracy,
        publish_min_accuracy=args.publish_min_accuracy,
        publish_min_time=args.publish_min_time,
        publish_max_time=args.publish_max_time,
        publish_min_memory=args.publish_min_memory,
        publish_max_memory=args.publish_max_memory,
    )
    print(f"Updated {args.readme} using {args.metrics}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[update_readme] ERROR: {exc}")
        raise
