#!/usr/bin/env python3
"""Update README performance metrics section from metrics.json.

Uses markers:
  <!-- METRICS_START -->
  <!-- METRICS_END -->
If markers are absent, they are appended to README.

When metrics are flagged as bad or below threshold, the existing metrics block is preserved
and a warning banner is inserted above it.
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

METRICS_START = "<!-- METRICS_START -->"
METRICS_END = "<!-- METRICS_END -->"
WARNING_START = "<!-- METRICS_WARNING_START -->"
WARNING_END = "<!-- METRICS_WARNING_END -->"


def _format_timestamp(metrics: Dict[str, Any]) -> str:
    source_ts = metrics.get("generated_at_utc")
    if isinstance(source_ts, str) and source_ts.strip():
        return source_ts
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def render_metrics_block(metrics: Dict[str, Any]) -> str:
    """Render markdown block inserted between metrics markers."""
    generated_at = _format_timestamp(metrics)
    accuracy = metrics.get("test_accuracy_percent", "N/A")
    train_time = metrics.get("training_time_seconds", "N/A")
    peak_memory = metrics.get("peak_memory_mb", "N/A")
    epochs = metrics.get("epochs", "N/A")
    dataset = metrics.get("dataset", "N/A")

    return (
        "## Performance Metrics\n\n"
        "Latest automated benchmark run:\n\n"
        "| Metric | Value |\n"
        "|---|---:|\n"
        f"| Final test accuracy (%) | {accuracy} |\n"
        f"| Total training time (seconds) | {train_time} |\n"
        f"| Peak memory usage (MB) | {peak_memory} |\n"
        f"| Epochs | {epochs} |\n"
        f"| Dataset source | {dataset} |\n\n"
        f"_Last metrics payload timestamp: {generated_at}_\n"
    )


def _default_metrics_placeholder() -> str:
    return (
        "## Performance Metrics\n\n"
        "Latest automated benchmark run:\n\n"
        "_No known good metrics are available yet._\n"
    )


def render_warning(accuracy: Any, min_acceptable_accuracy: float, reason: Optional[str] = None) -> str:
    """Render warning shown above preserved metrics on bad runs."""
    if isinstance(accuracy, (int, float)):
        accuracy_text = f"{float(accuracy):.4f}"
    else:
        accuracy_text = "N/A"

    reason_suffix = f" Reason: {reason}." if reason else ""
    return (
        f"{WARNING_START}\n"
        "⚠️ Warning: The latest automated benchmark produced unreliable results "
        f"(accuracy = {accuracy_text}%; minimum acceptable = {min_acceptable_accuracy:.2f}%). "
        "The model may need debugging. The last known good numbers are shown below."
        f"{reason_suffix}\n"
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


def _load_metrics(metrics_path: Path) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    if not metrics_path.exists():
        return None, f"Metrics file not found: {metrics_path}"
    try:
        return json.loads(metrics_path.read_text(encoding="utf-8")), None
    except Exception as exc:  # malformed json etc.
        return None, f"Could not parse metrics file: {exc}"


def update_readme(readme_path: Path, metrics_path: Path, min_acceptable_accuracy: float) -> None:
    """Inject (or create) the metrics section in README using markers."""
    if not readme_path.exists():
        raise FileNotFoundError(f"README file not found: {readme_path}")
    if min_acceptable_accuracy < 0.0 or min_acceptable_accuracy > 100.0:
        raise ValueError("--min-acceptable-accuracy must be between 0 and 100")

    metrics, load_error = _load_metrics(metrics_path)

    readme = readme_path.read_text(encoding="utf-8")
    readme = _remove_existing_warning(readme)

    bad_metrics = False
    accuracy: Any = None
    reason: Optional[str] = None

    if metrics is None:
        bad_metrics = True
        reason = load_error
    else:
        accuracy = metrics.get("test_accuracy_percent")
        below_threshold = isinstance(accuracy, (int, float)) and float(accuracy) < min_acceptable_accuracy
        flagged_bad = bool(metrics.get("bad_metrics", False))
        bad_metrics = flagged_bad or below_threshold
        if flagged_bad:
            reason = "metrics.json marked this run as bad"
        elif below_threshold:
            reason = "accuracy below threshold"

    if bad_metrics:
        if METRICS_START not in readme or METRICS_END not in readme:
            readme = _upsert_metrics_section(readme, _default_metrics_placeholder())
        warning = render_warning(accuracy, min_acceptable_accuracy, reason=reason)
        insert_at = readme.index(METRICS_START)
        updated = readme[:insert_at] + warning + readme[insert_at:]
    else:
        rendered = render_metrics_block(metrics or {})
        updated = _upsert_metrics_section(readme, rendered)

    readme_path.write_text(updated + ("\n" if not updated.endswith("\n") else ""), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update README metrics section from JSON.")
    parser.add_argument("--metrics", type=Path, default=Path("metrics.json"), help="Path to metrics.json")
    parser.add_argument("--readme", type=Path, default=Path("README.md"), help="Path to README.md")
    parser.add_argument(
        "--min-acceptable-accuracy",
        type=float,
        default=80.0,
        help="Minimum acceptable test accuracy. If accuracy is lower, preserve old metrics and add warning.",
    )
    args = parser.parse_args()

    update_readme(
        readme_path=args.readme,
        metrics_path=args.metrics,
        min_acceptable_accuracy=args.min_acceptable_accuracy,
    )
    print(f"Updated {args.readme} using {args.metrics}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[update_readme] ERROR: {exc}")
        raise
