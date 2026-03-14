"""Utility functions for hardware design space that do not depend on generated tables."""
from __future__ import annotations


def estimate_from_table(flops: float, bytes_moved: float, row_id: int = 0) -> dict[str, float]:
    """
    Estimate latency and energy using a pre-computed calibration table.
    This function loads the table from the generated research_tables module.
    """
    from .research_tables import calibration_table  # generated, may be absent until generated

    rows = calibration_table()
    row = rows[row_id % len(rows)]
    peak_ops = row["array_rows"] * row["array_cols"] * row["clock_mhz"] * 1e6 * 2 * row["macro_eff"]
    bw = row["bw_gbps"] * 1e9 / 8
    compute_s = flops / max(peak_ops, 1.0)
    mem_s = bytes_moved / max(bw, 1.0)
    latency_s = max(compute_s, mem_s)
    energy_j = flops * (0.3e-12 * (row["voltage_v"] / 0.8) ** 2) + bytes_moved * (2.8e-12 * (row["voltage_v"] / 0.8) ** 2)
    return {"latency_s": float(latency_s), "energy_j": float(energy_j), "row_id": float(row["id"])}


def calibration_table() -> list[dict[str, float]]:
    """
    Return the full calibration table. This is a stub that delegates to the generated module.
    """
    from .research_tables import calibration_table as _ct
    return _ct()
