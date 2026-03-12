#!/usr/bin/env python3
"""Local installer for generated phase-2 skills.

This script emulates skill installation by validating each generated skill
and confirming all declared repository targets exist.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = root / "skills" / "skill-manifest.json"
    data = json.loads(manifest.read_text())

    for skill_name in data:
        checker = root / "skills" / skill_name / "scripts" / "check_targets.py"
        print(f"[install] {skill_name}")
        subprocess.run(["python", str(checker)], check=True, cwd=root)

    print(f"Installed/validated {len(data)} skills.")


if __name__ == "__main__":
    main()
