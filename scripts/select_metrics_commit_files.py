#!/usr/bin/env python3
"""Select commit-safe metrics artifact files that exist and are not git-ignored."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def _is_ignored(path: Path) -> bool:
    proc = subprocess.run(["git", "check-ignore", "-q", str(path)], capture_output=True)
    return proc.returncode == 0


def _has_changes(path: Path) -> bool:
    proc = subprocess.run(["git", "status", "--porcelain", "--", str(path)], capture_output=True, text=True)
    return bool(proc.stdout.strip())


def select_commit_files(candidates: list[str]) -> list[str]:
    selected: list[str] = []
    for candidate in candidates:
        p = Path(candidate)
        if not p.exists():
            continue
        if _is_ignored(p):
            continue
        if _has_changes(p):
            selected.append(candidate)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description="Print changed, non-ignored metric files safe to commit")
    parser.add_argument("files", nargs="*", default=["README.md", "metrics.json", "artifacts/metrics_report.md", "artifacts/last_good_metrics.json"])
    args = parser.parse_args()

    selected = select_commit_files(args.files)
    for path in selected:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
