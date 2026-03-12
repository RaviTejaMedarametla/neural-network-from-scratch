from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class HardwareConstraint:
    max_latency_ms: float
    max_power_w: float
    max_energy_mj: float
    min_utilization: float


@dataclass
class HardwareObjectiveWeights:
    accuracy: float = 0.40
    latency: float = 0.20
    energy: float = 0.20
    throughput: float = 0.10
    utilization: float = 0.10


@dataclass
class ResearchMetricBundle:
    accuracy: float
    latency_ms: float
    energy_mj: float
    throughput_sps: float
    utilization: float
    roofline_efficiency: float
    energy_delay_product: float
    objective: float


def roofline_efficiency(achieved_tops: float, peak_tops: float) -> float:
    return float(np.clip(achieved_tops / max(peak_tops, 1e-12), 0.0, 1.0))


def energy_delay_product(energy_mj: float, latency_ms: float) -> float:
    return float(energy_mj * latency_ms)


def constraint_violations(bundle: ResearchMetricBundle, c: HardwareConstraint) -> dict[str, float]:
    return {
        "latency_ms": max(0.0, bundle.latency_ms - c.max_latency_ms),
        "power_w": 0.0,  # Optional power field not required in bundle.
        "energy_mj": max(0.0, bundle.energy_mj - c.max_energy_mj),
        "utilization": max(0.0, c.min_utilization - bundle.utilization),
    }


def objective_score(
    accuracy: float,
    latency_ms: float,
    energy_mj: float,
    throughput_sps: float,
    utilization: float,
    weights: HardwareObjectiveWeights | None = None,
) -> float:
    w = weights or HardwareObjectiveWeights()
    acc_term = np.clip(accuracy, 0.0, 1.0)
    lat_term = 1.0 / (1.0 + latency_ms)
    en_term = 1.0 / (1.0 + energy_mj)
    thr_term = 1.0 - np.exp(-throughput_sps / 2000.0)
    util_term = np.clip(utilization, 0.0, 1.0)
    return float(
        w.accuracy * acc_term
        + w.latency * lat_term
        + w.energy * en_term
        + w.throughput * thr_term
        + w.utilization * util_term
    )


def build_metric_bundle(
    accuracy: float,
    latency_ms: float,
    energy_mj: float,
    throughput_sps: float,
    utilization: float,
    achieved_tops: float,
    peak_tops: float,
    weights: HardwareObjectiveWeights | None = None,
) -> ResearchMetricBundle:
    roof = roofline_efficiency(achieved_tops, peak_tops)
    edp = energy_delay_product(energy_mj, latency_ms)
    obj = objective_score(accuracy, latency_ms, energy_mj, throughput_sps, utilization, weights)
    return ResearchMetricBundle(
        accuracy=accuracy,
        latency_ms=latency_ms,
        energy_mj=energy_mj,
        throughput_sps=throughput_sps,
        utilization=utilization,
        roofline_efficiency=roof,
        energy_delay_product=edp,
        objective=obj,
    )
