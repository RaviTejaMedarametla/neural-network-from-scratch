from __future__ import annotations

from dataclasses import asdict, dataclass

from .cycle_accurate import CycleAccurateHardwareModel


@dataclass
class HardwareTarget:
    name: str
    mac_units: int
    clock_speed_hz: float
    memory_bandwidth_bps: float
    energy_per_mac_j: float
    energy_per_byte_j: float


CortexM4 = HardwareTarget("CortexM4", mac_units=1, clock_speed_hz=120e6,
                          memory_bandwidth_bps=300e6, energy_per_mac_j=2e-10, energy_per_byte_j=5e-11)
EdgeTPU = HardwareTarget("EdgeTPU", mac_units=4096, clock_speed_hz=500e6,
                         memory_bandwidth_bps=16e9, energy_per_mac_j=2e-12, energy_per_byte_j=8e-12)
GenericGPU = HardwareTarget("GenericGPU", mac_units=16384, clock_speed_hz=1.5e9,
                            memory_bandwidth_bps=600e9, energy_per_mac_j=8e-12, energy_per_byte_j=3e-12)


class HardwareProfiler:
    """Profiler with both analytical and optional cycle-accurate modes."""

    def __init__(self, target: HardwareTarget = GenericGPU) -> None:
        self.target = target
        self.cycle_model: CycleAccurateHardwareModel | None = None
        self.reset()

    def reset(self) -> None:
        self.total_flops = 0
        self.total_bytes = 0

    def record_op(self, flops: int, bytes_moved: int) -> None:
        self.total_flops += int(flops)
        self.total_bytes += int(bytes_moved)

    def estimate_latency_s(self) -> float:
        compute = self.total_flops / max(self.target.mac_units * self.target.clock_speed_hz * 2, 1.0)
        memory = self.total_bytes / max(self.target.memory_bandwidth_bps, 1.0)
        return max(compute, memory)

    def estimate_energy_j(self) -> float:
        return self.total_flops / 2 * self.target.energy_per_mac_j + self.total_bytes * self.target.energy_per_byte_j

    def report(self) -> dict:
        return {
            "target": asdict(self.target),
            "total_flops": self.total_flops,
            "total_bytes": self.total_bytes,
            "latency_s": self.estimate_latency_s(),
            "energy_j": self.estimate_energy_j(),
        }

    def set_cycle_model(self, cycle_model: CycleAccurateHardwareModel) -> None:
        self.cycle_model = cycle_model

    def profile_model(self, model, input_shape: tuple[int, ...]) -> dict:
        self.reset()
        self.record_op(model.flops(input_shape), model.memory_footprint())
        analytical = self.report()
        if self.cycle_model is None:
            return analytical
        cycle = self.cycle_model.simulate_model(model, input_shape)
        return {**analytical, "cycle_accurate": cycle}

    def profile_model_cycle(self, model, input_shape: tuple[int, ...]) -> dict:
        if self.cycle_model is None:
            raise RuntimeError("Cycle-accurate model not set")
        return self.cycle_model.simulate_model(model, input_shape)
