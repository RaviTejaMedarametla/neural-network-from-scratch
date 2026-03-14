#!/usr/bin/env python3
"""Generate deterministic hardware table modules.

This script creates `src/hardware/design_space.py` and `src/hardware/research_tables.py`.
Generated files are intentionally gitignored so they can be regenerated locally.
"""

from __future__ import annotations

from pathlib import Path


DESIGN_SPACE_TEMPLATE = '''"""Auto-generated deterministic design points for hardware sweeps."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class DesignPoint:
    name: str
    mac_units: int
    frequency_ghz: float
    bandwidth_gbps: float


def all_points() -> list[DesignPoint]:
    return [
        DesignPoint("tiny", mac_units=128, frequency_ghz=0.6, bandwidth_gbps=64.0),
        DesignPoint("small", mac_units=256, frequency_ghz=0.8, bandwidth_gbps=96.0),
        DesignPoint("medium", mac_units=512, frequency_ghz=1.0, bandwidth_gbps=128.0),
        DesignPoint("large", mac_units=1024, frequency_ghz=1.2, bandwidth_gbps=192.0),
    ]
'''

RESEARCH_TABLES_TEMPLATE = '''"""Auto-generated deterministic calibration tables for hardware what-if analysis."""

from __future__ import annotations


def calibration_table() -> list[dict[str, float]]:
    return [
        {"id": 0.0, "latency_scale": 1.00, "energy_scale": 1.00},
        {"id": 1.0, "latency_scale": 0.85, "energy_scale": 0.92},
        {"id": 2.0, "latency_scale": 0.73, "energy_scale": 0.88},
        {"id": 3.0, "latency_scale": 0.62, "energy_scale": 0.84},
    ]


def estimate_from_table(flops: float, bytes_moved: float, row_id: int = 0) -> dict[str, float]:
    rows = calibration_table()
    idx = max(0, min(int(row_id), len(rows) - 1))
    row = rows[idx]
    latency_s = (flops / 1e9 + bytes_moved / 1e10) * row["latency_scale"]
    energy_j = (flops * 2e-12 + bytes_moved * 4e-12) * row["energy_scale"]
    return {"latency_s": float(latency_s), "energy_j": float(energy_j), "row_id": float(idx)}
'''


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    hw = root / "src" / "hardware"
    hw.mkdir(parents=True, exist_ok=True)

    design = hw / "design_space.py"
    research = hw / "research_tables.py"

    design.write_text(DESIGN_SPACE_TEMPLATE)
    research.write_text(RESEARCH_TABLES_TEMPLATE)

    print(f"generated: {design}")
    print(f"generated: {research}")


if __name__ == "__main__":
    main()
