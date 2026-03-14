#!/usr/bin/env python3
"""Regenerate large hardware table files (design_space.py, research_tables.py)."""

import sys
from pathlib import Path

# Add project root to path to import helpers if needed
sys.path.append(str(Path(__file__).resolve().parents[1]))

# ----------------------------------------------------------------------
# design_space.py – hardware design points
# ----------------------------------------------------------------------
DESIGN_SPACE_TEMPLATE = '''"""Auto-generated hardware design points. Do not edit manually."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DesignPoint:
    name: str
    mac_units: int
    frequency_ghz: float
    bandwidth_gbps: float
    sram_kb: int
    voltage_v: float


def all_points() -> list[DesignPoint]:
    return [
{points}
    ]


def pareto_front(model_flops: float, model_bytes: float) -> list[tuple[DesignPoint, dict]]:
    from .design_space import all_points  # local import to avoid circular deps
    pts = [(p, score_point(p, model_flops, model_bytes)) for p in all_points()]
    front = []
    for p, m in pts:
        dominated = False
        for p2, m2 in pts:
            if (m2["latency_s"] <= m["latency_s"] and m2["energy_j"] <= m["energy_j"] and
                (m2["latency_s"] < m["latency_s"] or m2["energy_j"] < m["energy_j"])):
                dominated = True
                break
        if not dominated:
            front.append((p, m))
    front.sort(key=lambda x: (x[1]["latency_s"], x[1]["energy_j"]))
    return front


def score_point(p: DesignPoint, model_flops: float, model_bytes: float) -> dict:
    peak_ops = p.mac_units * p.frequency_ghz * 2e9
    bw = p.bandwidth_gbps * 1e9 / 8.0
    t_compute = model_flops / max(peak_ops, 1.0)
    t_mem = model_bytes / max(bw, 1.0)
    latency = max(t_compute, t_mem)
    energy = model_flops * (0.4e-12 * (p.voltage_v/0.8)**2) + model_bytes * (3.2e-12 * (p.voltage_v/0.8)**2)
    return {{"latency_s": latency, "energy_j": energy}}
'''

def generate_design_space():
    points = []
    for i in range(700):
        mac_units = 128 + i * 32
        freq = 0.6 + i * 0.05
        bw = 64 + i * 16
        sram = 128 + i * 128
        volt = 0.65 + i * 0.03
        points.append(f'        DesignPoint("point_{i}", mac_units={mac_units}, frequency_ghz={freq:.2f}, bandwidth_gbps={bw}, sram_kb={sram}, voltage_v={volt:.2f}),')
    point_str = "\n".join(points)
    content = DESIGN_SPACE_TEMPLATE.format(points=point_str)
    Path("src/hardware/design_space.py").write_text(content)
    print("Generated src/hardware/design_space.py")

# ----------------------------------------------------------------------
# research_tables.py – calibration rows
# ----------------------------------------------------------------------
RESEARCH_TABLES_TEMPLATE = '''"""Auto-generated research calibration tables. Do not edit manually."""
from __future__ import annotations


{rows}


def calibration_table() -> list[dict[str, float]]:
    return [
{list}
    ]


def estimate_from_table(flops: float, bytes_moved: float, row_id: int = 0) -> dict[str, float]:
    rows = calibration_table()
    row = rows[row_id % len(rows)]
    peak_ops = row["array_rows"] * row["array_cols"] * row["clock_mhz"] * 1e6 * 2 * row["macro_eff"]
    bw = row["bw_gbps"] * 1e9 / 8
    compute_s = flops / max(peak_ops, 1.0)
    mem_s = bytes_moved / max(bw, 1.0)
    latency_s = max(compute_s, mem_s)
    energy_j = flops * (0.3e-12 * (row["voltage_v"]/0.8)**2) + bytes_moved * (2.8e-12 * (row["voltage_v"]/0.8)**2)
    return {{"latency_s": float(latency_s), "energy_j": float(energy_j), "row_id": float(row["id"])}}
'''

def generate_research_tables():
    rows_def = []
    rows_list = []
    for i in range(1200):
        row_id = i
        array_rows = 8 + (i % 32)
        array_cols = 8 + (i // 32) * 3
        clock_mhz = 200 + (i % 600)
        bw_gbps = 16 + (i % 90)
        voltage_v = 0.55 + (i % 40) * 0.01
        leakage_mw = 20 + (i % 80)
        temp_c = 25 + (i % 60)
        macro_eff = 0.45 + (i % 40) * 0.015
        macro_eff = min(macro_eff, 0.885)  # cap at original max
        rows_def.append(
            f'def calibration_row_{i}() -> dict[str, float]:\n'
            f'    return {{"id": {row_id}, "array_rows": {array_rows}, "array_cols": {array_cols}, '
            f'"clock_mhz": {clock_mhz}, "bw_gbps": {bw_gbps}, "voltage_v": {voltage_v:.2f}, '
            f'"leakage_mw": {leakage_mw}, "temp_c": {temp_c}, "macro_eff": {macro_eff:.3f}}}'
        )
        rows_list.append(f'        calibration_row_{i}(),')
    rows_def_str = "\n\n".join(rows_def)
    rows_list_str = "\n".join(rows_list)
    content = RESEARCH_TABLES_TEMPLATE.format(rows=rows_def_str, list=rows_list_str)
    Path("src/hardware/research_tables.py").write_text(content)
    print("Generated src/hardware/research_tables.py")

if __name__ == "__main__":
    generate_design_space()
    generate_research_tables()
