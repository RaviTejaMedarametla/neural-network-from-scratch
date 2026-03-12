from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.hardware import HardwareObjectiveWeights, build_metric_bundle


@dataclass
class StudyResult:
    name: str
    accuracy: float
    latency_ms: float
    energy_mj: float
    throughput_sps: float
    utilization: float
    objective: float


class HardwareOptimizationStudy:
    """Runs hardware/model sweeps and ranks by multi-objective score."""

    def __init__(self, weights: HardwareObjectiveWeights | None = None) -> None:
        self.weights = weights or HardwareObjectiveWeights()

    def evaluate_candidate(
        self,
        name: str,
        accuracy: float,
        latency_ms: float,
        energy_mj: float,
        throughput_sps: float,
        utilization: float,
        achieved_tops: float,
        peak_tops: float,
    ) -> StudyResult:
        bundle = build_metric_bundle(
            accuracy=accuracy,
            latency_ms=latency_ms,
            energy_mj=energy_mj,
            throughput_sps=throughput_sps,
            utilization=utilization,
            achieved_tops=achieved_tops,
            peak_tops=peak_tops,
            weights=self.weights,
        )
        return StudyResult(
            name=name,
            accuracy=bundle.accuracy,
            latency_ms=bundle.latency_ms,
            energy_mj=bundle.energy_mj,
            throughput_sps=bundle.throughput_sps,
            utilization=bundle.utilization,
            objective=bundle.objective,
        )

    def rank(self, results: list[StudyResult]) -> list[StudyResult]:
        return sorted(results, key=lambda x: x.objective, reverse=True)

    def summarize(self, results: list[StudyResult]) -> dict[str, float]:
        if not results:
            return {"count": 0.0, "best_objective": 0.0, "mean_objective": 0.0}
        vals = np.array([r.objective for r in results], dtype=np.float64)
        return {
            "count": float(len(results)),
            "best_objective": float(vals.max()),
            "mean_objective": float(vals.mean()),
            "std_objective": float(vals.std()),
        }
