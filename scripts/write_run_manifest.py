"""Write a reproducibility manifest for experiment runs."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _git_sha(repo_root: Path) -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True)
        return out.strip()
    except Exception:
        return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description="Persist run metadata for reproducibility")
    parser.add_argument("--experiment", required=True, help="Experiment identifier or config name")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="experiments/manifests", help="Output directory")
    parser.add_argument("--notes", default="", help="Optional short note")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "experiment": args.experiment,
        "seed": args.seed,
        "git_sha": _git_sha(repo_root),
        "python": sys.version,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "notes": args.notes,
    }

    name = f"{args.experiment.replace('/', '_')}_seed{args.seed}.json"
    out_path = out_dir / name
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote reproducibility manifest: {out_path}")


if __name__ == "__main__":
    main()
