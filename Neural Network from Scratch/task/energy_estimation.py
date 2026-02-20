"""Simple runtime and FLOPs-inspired energy estimation utilities."""

from __future__ import annotations

from typing import Iterable

PRECISION_POWER_W = {
    "float32": 45.0,
    "float16": 35.0,
    "int8": 25.0,
}


def estimate_runtime_energy_j(runtime_seconds: float, precision_mode: str = "float32") -> float:
    """Estimate energy via power*time using precision-dependent nominal CPU power."""
    power = PRECISION_POWER_W.get(precision_mode, PRECISION_POWER_W["float32"])
    return float(runtime_seconds) * power


def estimate_dense_flops(layer_sizes: Iterable[int], batch_size: int) -> int:
    """Estimate FLOPs for dense forward pass (multiply+add approximated as 2 FLOPs)."""
    sizes = list(layer_sizes)
    total = 0
    for i in range(len(sizes) - 1):
        total += 2 * int(batch_size) * int(sizes[i]) * int(sizes[i + 1])
    return total


def estimate_flops_energy_j(flops: int, joules_per_gflop: float = 0.05) -> float:
    """Estimate energy from FLOPs using configurable joules/GFLOP coefficient."""
    gflops = float(flops) / 1e9
    return gflops * float(joules_per_gflop)
