from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Accelerator:
    array_rows: int = 32
    array_cols: int = 32
    frequency_hz: float = 400e6
    bytes_per_cycle: int = 32
    energy_per_cycle_j: float = 3e-10

    def simulate_layer(self, layer, input_shape: tuple[int, ...]) -> dict:
        flops = layer.flops(input_shape)
        mem = layer.memory_footprint()
        macs = flops / 2
        cycles_compute = macs / max(self.array_rows * self.array_cols, 1)
        cycles_memory = mem / max(self.bytes_per_cycle, 1)
        cycles = max(cycles_compute, cycles_memory)
        latency = cycles / self.frequency_hz
        energy = cycles * self.energy_per_cycle_j
        return {"cycles": cycles, "latency_s": latency, "energy_j": energy, "flops": flops, "memory_bytes": mem}
