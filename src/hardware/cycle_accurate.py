from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

from .energy_model import EnergyModel, TSMC28nmEnergy


class PipelineStage(ABC):
    """Abstract pipeline stage."""

    @abstractmethod
    def tick(self) -> None:
        """Advance one cycle."""


@dataclass
class CPUStats:
    cycles: float
    energy_j: float


class SimpleCPU:
    """Simple 5-stage in-order CPU model."""

    def __init__(
        self,
        clock_speed_hz: float = 1e9,
        mac_units: int = 1,
        energy_model: EnergyModel | None = None,
    ) -> None:
        self.clock_speed_hz = clock_speed_hz
        self.mac_units = mac_units
        self.energy_model = energy_model or TSMC28nmEnergy()
        self.cycles = 0.0

    def simulate_layer(self, layer: Any, input_shape: tuple[int, ...]) -> CPUStats:
        flops = float(layer.flops(input_shape))
        macs = flops / 2.0
        cycles = macs / max(self.mac_units, 1)
        self.cycles += cycles
        energy_j = macs * self.energy_model.energy_per_mac_pj() * 1e-12
        return CPUStats(cycles=cycles, energy_j=energy_j)


@dataclass
class SystolicStats:
    cycles: float
    utilization: float


class SystolicArray:
    """Systolic array simulator for GEMM-like workloads."""

    def __init__(self, rows: int = 16, cols: int = 16, frequency_hz: float = 500e6) -> None:
        self.rows = rows
        self.cols = cols
        self.frequency_hz = frequency_hz
        self.cycles = 0.0

    def simulate_matmul(self, m: int, n: int, k: int) -> SystolicStats:
        total_macs = float(m * n * k)
        peak = float(self.rows * self.cols)
        cycles = total_macs / max(peak, 1.0)
        self.cycles += cycles
        wavefront_penalty = (self.rows + self.cols) / max(m + n, 1)
        util = max(0.05, min(1.0, 1.0 - wavefront_penalty))
        return SystolicStats(cycles=cycles, utilization=util)


class MemoryController:
    """DRAM + cache transfer model."""

    def __init__(self, dram_bandwidth_gbps: float = 25.6, cache_line_bytes: int = 64) -> None:
        self.bandwidth_bps = dram_bandwidth_gbps * 1e9
        self.cache_line_bytes = cache_line_bytes

    def transfer_time(self, num_bytes: int) -> float:
        return num_bytes / max(self.bandwidth_bps, 1.0)


class CycleAccurateHardwareModel:
    """Composite cycle-accurate model across CPU/accelerator/memory."""

    def __init__(self, cpu: SimpleCPU, accelerator: SystolicArray, memory: MemoryController) -> None:
        self.cpu = cpu
        self.accelerator = accelerator
        self.memory = memory

    def _layer_transfer_bytes(self, layer: Any) -> int:
        if hasattr(layer, "memory_footprint"):
            return int(layer.memory_footprint())
        return 0

    def _prefer_accelerator(self, layer: Any) -> bool:
        name = layer.__class__.__name__.lower()
        return any(token in name for token in ["dense", "conv", "attention", "transformer"])

    def simulate_model(self, model: Any, input_shape: tuple[int, ...]) -> dict[str, float]:
        total_cycles = 0.0
        total_energy = 0.0
        total_mem_time = 0.0
        accel_cycles = 0.0
        cpu_cycles = 0.0
        utilization_samples: list[float] = []

        for layer in model.layers:
            bytes_moved = self._layer_transfer_bytes(layer)
            total_mem_time += self.memory.transfer_time(bytes_moved)

            if self._prefer_accelerator(layer):
                if hasattr(layer, "w") and isinstance(layer.w, np.ndarray) and layer.w.ndim == 2:
                    m = input_shape[0]
                    k, n = layer.w.shape
                    stats = self.accelerator.simulate_matmul(m, n, k)
                else:
                    flops = float(layer.flops(input_shape))
                    pseudo_m = max(1, int(np.sqrt(flops / 2)))
                    stats = self.accelerator.simulate_matmul(pseudo_m, pseudo_m, max(1, pseudo_m // 2))
                accel_cycles += stats.cycles
                total_cycles += stats.cycles
                utilization_samples.append(stats.utilization)
                total_energy += stats.cycles * 1e-12
            else:
                stats_cpu = self.cpu.simulate_layer(layer, input_shape)
                cpu_cycles += stats_cpu.cycles
                total_cycles += stats_cpu.cycles
                total_energy += stats_cpu.energy_j
                utilization_samples.append(0.0)

        latency_s = total_cycles / max(self.cpu.clock_speed_hz, 1.0) + total_mem_time
        return {
            "cycles_total": float(total_cycles),
            "cycles_cpu": float(cpu_cycles),
            "cycles_accelerator": float(accel_cycles),
            "latency_s": float(latency_s),
            "memory_time_s": float(total_mem_time),
            "energy_j": float(total_energy),
            "accelerator_utilization": float(np.mean(utilization_samples) if utilization_samples else 0.0),
        }
