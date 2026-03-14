#!/usr/bin/env python3
"""Regenerate hardware table files used by the hardware package."""

from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    hw = root / "src" / "hardware"
    design = hw / "design_space.py"
    research = hw / "research_tables.py"

    # Keep this script intentionally conservative to avoid accidental drift:
    # if files already exist, report status; if missing, write minimal stubs.
    if design.exists() and research.exists():
        print("design_space.py and research_tables.py already present; no rewrite performed")
        return

    if not design.exists():
        design.write_text('"""Auto-generated deterministic design points for hardware sweeps."""\n\nfrom __future__ import annotations\n\ndef all_points() -> list:\n    return []\n')
        print(f"generated: {design}")

    if not research.exists():
        research.write_text('"""Auto-generated deterministic calibration tables for hardware what-if analysis."""\n\nfrom __future__ import annotations\n\ndef calibration_table() -> list[dict[str, float]]:\n    return []\n\ndef estimate_from_table(flops: float, bytes_moved: float, row_id: int = 0) -> dict[str, float]:\n    return {\"latency_s\": 0.0, \"energy_j\": 0.0, \"row_id\": float(row_id)}\n')
        print(f"generated: {research}")


if __name__ == "__main__":
    main()
