#!/usr/bin/env python3
"""Generate deterministic hardware sweep tables."""

from __future__ import annotations

from pathlib import Path


def write_design_space(path: Path, points: int = 128) -> None:
    lines = [
        'from __future__ import annotations\n',
        'from dataclasses import dataclass\n\n',
        '"""Auto-generated deterministic design points for hardware sweeps."""\n\n',
        '@dataclass\n',
        'class DesignPoint:\n',
        '    name: str\n',
        '    mac_units: int\n',
        '    frequency_ghz: float\n',
        '    bandwidth_gbps: float\n',
        '    sram_kb: int\n',
        '    voltage_v: float\n\n',
        'def score_point(p: DesignPoint, model_flops: float, model_bytes: float) -> dict:\n',
        '    peak_ops = p.mac_units * p.frequency_ghz * 2e9\n',
        '    bw = p.bandwidth_gbps * 1e9 / 8.0\n',
        '    t_compute = model_flops / max(peak_ops, 1.0)\n',
        '    t_mem = model_bytes / max(bw, 1.0)\n',
        '    latency = max(t_compute, t_mem)\n',
        '    energy = model_flops * (0.4e-12 * (p.voltage_v / 0.8) ** 2) + model_bytes * (3.2e-12 * (p.voltage_v / 0.8) ** 2)\n',
        '    throughput = 1.0 / max(latency, 1e-12)\n',
        '    return {"latency_s": latency, "energy_j": energy, "throughput": throughput}\n\n',
    ]
    for i in range(points):
        lines.append(
            f'def point_{i}() -> DesignPoint:\n'
            f'    return DesignPoint("point_{i}", mac_units={128 + (i % 32) * 32}, frequency_ghz={0.6 + (i % 10) * 0.05:.3f}, bandwidth_gbps={64 + (i % 16) * 8}, sram_kb={128 + (i % 12) * 64}, voltage_v={0.65 + (i % 9) * 0.03:.2f})\n\n'
        )
    lines.append('def all_points() -> list[DesignPoint]:\n')
    lines.append(f'    return [{", ".join([f"point_{i}()" for i in range(points)])}]\n')
    path.write_text(''.join(lines))


def write_research_tables(path: Path, rows: int = 256) -> None:
    lines = [
        'from __future__ import annotations\n\n',
        '"""Auto-generated deterministic calibration rows for hardware what-if analysis."""\n\n',
        'def calibration_table() -> list[dict[str, float]]:\n',
        '    rows: list[dict[str, float]] = []\n',
        f'    for i in range({rows}):\n',
        '        rows.append({\n',
        '            "id": float(i),\n',
        '            "array_rows": float(8 + (i % 32)),\n',
        '            "array_cols": float(8 + ((i * 3) % 32)),\n',
        '            "clock_mhz": float(200 + (i % 20) * 20),\n',
        '            "bw_gbps": float(16 + (i % 20) * 4),\n',
        '            "voltage_v": float(0.55 + (i % 15) * 0.02),\n',
        '            "leakage_mw": float(20 + i % 80),\n',
        '            "temp_c": float(25 + i % 60),\n',
        '            "macro_eff": float(min(0.95, 0.45 + 0.005 * i)),\n',
        '        })\n',
        '    return rows\n\n',
        'def estimate_from_table(flops: float, bytes_moved: float, row_id: int = 0) -> dict[str, float]:\n',
        '    rows = calibration_table()\n',
        '    row = rows[max(0, min(int(row_id), len(rows) - 1))]\n',
        '    peak_ops = row["array_rows"] * row["array_cols"] * row["clock_mhz"] * 1e6\n',
        '    bw = row["bw_gbps"] * 1e9 / 8.0\n',
        '    latency_s = max(flops / max(peak_ops, 1.0), bytes_moved / max(bw, 1.0))\n',
        '    energy_j = flops * 1e-12 * row["macro_eff"] + bytes_moved * 3e-12\n',
        '    return {"row": row, "latency_s": latency_s, "energy_j": energy_j}\n',
    ]
    path.write_text(''.join(lines))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    hw = root / 'src' / 'hardware'
    hw.mkdir(parents=True, exist_ok=True)
    write_design_space(hw / 'design_space.py')
    write_research_tables(hw / 'research_tables.py')
    print('generated src/hardware/design_space.py and src/hardware/research_tables.py')


if __name__ == '__main__':
    main()
