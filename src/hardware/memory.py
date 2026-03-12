from __future__ import annotations
from dataclasses import dataclass


@dataclass
class MemoryLevel:
    name: str
    size_bytes: int
    bandwidth_bps: float
    energy_per_byte_j: float


class MemoryHierarchy:
    def __init__(self) -> None:
        self.levels = [
            MemoryLevel("l1", 64 * 1024, 100e9, 5e-12),
            MemoryLevel("sram", 2 * 1024 * 1024, 20e9, 2e-11),
            MemoryLevel("dram", 2**30, 8e9, 8e-11),
        ]

    def access_cost(self, bytes_accessed: int) -> dict:
        remaining = bytes_accessed
        latency = 0.0
        energy = 0.0
        detail = {}
        for lvl in self.levels:
            moved = min(remaining, lvl.size_bytes)
            remaining -= moved
            latency += moved / lvl.bandwidth_bps
            energy += moved * lvl.energy_per_byte_j
            detail[lvl.name] = moved
            if remaining <= 0:
                break
        if remaining > 0:
            last = self.levels[-1]
            latency += remaining / last.bandwidth_bps
            energy += remaining * last.energy_per_byte_j
            detail[last.name] = detail.get(last.name, 0) + remaining
        return {"latency_s": latency, "energy_j": energy, "detail": detail}
