from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .config import HardwareConfig, ModelConfig, TrainingConfig


@dataclass(slots=True)
class LayerHardwareStats:
    layer_name: str
    ops: float
    parameter_bytes: float
    activation_bytes: float
    intensity: float
    estimated_cycles: float
    energy_nj: float
    utilization: float


@dataclass(slots=True)
class HardwareReport:
    total_ops: float
    total_parameter_bytes: float
    total_activation_bytes: float
    weighted_intensity: float
    estimated_latency_ms: float
    estimated_throughput_samples_s: float
    estimated_power_w: float
    estimated_energy_mj_per_batch: float
    memory_bound_fraction: float
    compute_bound_fraction: float
    achieved_tops: float
    roofline_tops: float
    tdp_headroom_w: float
    layer_stats: list[LayerHardwareStats]

    def to_dict(self) -> dict:
        base = asdict(self)
        base["layer_stats"] = [asdict(v) for v in self.layer_stats]
        return base


class HardwareEstimator:
    """
    Heuristic hardware estimator for dense neural network workloads.

    Not a cycle-accurate simulator; intended for comparative research and design-space
    exploration with traceable formulas.
    """

    def __init__(self, hw: HardwareConfig):
        self.hw = hw

    @property
    def bytes_per_elem(self) -> int:
        return max(1, self.hw.precision_bits // 8)

    @property
    def peak_tops(self) -> float:
        # each MAC counts as 2 ops
        return 2.0 * self.hw.mac_units * self.hw.frequency_ghz / 1e3

    @property
    def peak_mem_gbs(self) -> float:
        return self.hw.hbm_bandwidth_gbps / 8.0

    def _noc_penalty(self) -> float:
        if self.hw.noc_topology == "mesh":
            return 1.0
        if self.hw.noc_topology == "torus":
            return 0.92
        if self.hw.noc_topology == "crossbar":
            return 1.08
        return 1.0

    def _sparsity_gain(self) -> float:
        if not self.hw.sparsity_support:
            return 1.0
        if self.hw.precision_bits <= 8:
            return 1.25
        return 1.12

    def _precision_energy_scale(self) -> float:
        if self.hw.precision_bits == 4:
            return 0.45
        if self.hw.precision_bits == 8:
            return 0.62
        if self.hw.precision_bits == 16:
            return 0.84
        return 1.0

    def _voltage_energy_scale(self) -> float:
        return (self.hw.voltage_v / 0.78) ** 2

    def estimate_layer(
        self,
        batch_size: int,
        in_dim: int,
        out_dim: int,
        name: str,
    ) -> LayerHardwareStats:
        ops = float(batch_size * in_dim * out_dim * 2)
        param_bytes = float(in_dim * out_dim * self.bytes_per_elem)
        activation_bytes = float(batch_size * (in_dim + out_dim) * self.bytes_per_elem)

        moved = param_bytes + activation_bytes
        intensity = ops / max(moved, 1.0)

        compute_time_s = ops / (self.peak_tops * 1e12 * self.hw.utilization_target * self._noc_penalty() * self._sparsity_gain())
        mem_time_s = moved / (self.peak_mem_gbs * 1e9)
        total_time_s = max(compute_time_s, mem_time_s)
        cycles = total_time_s * self.hw.frequency_ghz * 1e9

        # simple energy model
        energy_mac_pj = 0.45 * self._precision_energy_scale() * self._voltage_energy_scale()
        energy_mem_pj = 2.5 * self._precision_energy_scale() * self._voltage_energy_scale()
        energy_nj = (ops / 2.0) * energy_mac_pj * 1e-3 + moved * energy_mem_pj * 1e-3

        utilization = min(1.0, compute_time_s / (mem_time_s + compute_time_s + 1e-12) * 1.9)

        return LayerHardwareStats(
            layer_name=name,
            ops=ops,
            parameter_bytes=param_bytes,
            activation_bytes=activation_bytes,
            intensity=float(intensity),
            estimated_cycles=float(cycles),
            energy_nj=float(energy_nj),
            utilization=float(utilization),
        )

    def estimate_network(
        self,
        model: ModelConfig,
        training: TrainingConfig,
    ) -> HardwareReport:
        dims = [model.input_dim, *model.hidden_dims, model.output_dim]
        layer_stats: list[LayerHardwareStats] = []

        for i in range(len(dims) - 1):
            layer_stats.append(
                self.estimate_layer(
                    batch_size=training.batch_size,
                    in_dim=dims[i],
                    out_dim=dims[i + 1],
                    name=f"dense_{i}",
                )
            )

        total_ops = float(sum(x.ops for x in layer_stats))
        total_param_b = float(sum(x.parameter_bytes for x in layer_stats))
        total_activation_b = float(sum(x.activation_bytes for x in layer_stats))

        weighted_intensity = total_ops / max(total_param_b + total_activation_b, 1.0)
        roofline_tops = min(self.peak_tops, self.peak_mem_gbs * weighted_intensity / 1e3)

        layer_times_s = [x.estimated_cycles / (self.hw.frequency_ghz * 1e9) for x in layer_stats]
        latency_s = float(sum(layer_times_s))
        throughput = training.batch_size / max(latency_s, 1e-9)

        # estimate power
        total_energy_mj = sum(x.energy_nj for x in layer_stats) * 1e-6
        power_w = (total_energy_mj * 1e-3) / max(latency_s, 1e-12)
        power_w = min(self.hw.tdp_watts * 1.05, power_w)

        memory_bound_fraction = float(np.mean([
            (x.parameter_bytes + x.activation_bytes) / (x.ops + 1e-6) > 0.02 for x in layer_stats
        ]))
        compute_bound_fraction = 1.0 - memory_bound_fraction

        achieved_tops = (total_ops / max(latency_s, 1e-12)) / 1e12
        tdp_headroom = self.hw.tdp_watts - power_w

        return HardwareReport(
            total_ops=total_ops,
            total_parameter_bytes=total_param_b,
            total_activation_bytes=total_activation_b,
            weighted_intensity=float(weighted_intensity),
            estimated_latency_ms=latency_s * 1e3,
            estimated_throughput_samples_s=float(throughput),
            estimated_power_w=float(power_w),
            estimated_energy_mj_per_batch=float(total_energy_mj),
            memory_bound_fraction=float(memory_bound_fraction),
            compute_bound_fraction=float(compute_bound_fraction),
            achieved_tops=float(achieved_tops),
            roofline_tops=float(roofline_tops),
            tdp_headroom_w=float(tdp_headroom),
            layer_stats=layer_stats,
        )


def hardware_efficiency_score(report: HardwareReport, hw: HardwareConfig) -> float:
    perf_score = min(1.0, report.achieved_tops / max(report.roofline_tops, 1e-9))
    energy_score = np.exp(-report.estimated_energy_mj_per_batch / 2.5)
    power_score = max(0.0, min(1.0, report.tdp_headroom_w / max(hw.tdp_watts, 1e-6) + 0.5))
    balance_score = 1.0 - abs(report.memory_bound_fraction - 0.5)

    return float(0.4 * perf_score + 0.25 * energy_score + 0.2 * power_score + 0.15 * balance_score)
