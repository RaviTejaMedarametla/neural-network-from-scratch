"""Hardware exports."""

from .profiler import HardwareProfiler, HardwareTarget, CortexM4, EdgeTPU, GenericGPU
from .quantization import Quantizer, quantization_error
from .memory import MemoryHierarchy
from .accelerator import Accelerator
from .cycle_accurate import CycleAccurateHardwareModel, MemoryController, SimpleCPU, SystolicArray
from .energy_model import EnergyModel, TSMC28nmEnergy, TSMC7nmEnergy
try:
    from .research_tables import calibration_table, estimate_from_table
except ModuleNotFoundError:
    def calibration_table() -> list[dict[str, float]]:
        return []

    def estimate_from_table(flops: float, bytes_moved: float, row_id: int = 0) -> dict[str, float]:
        return {"latency_s": 0.0, "energy_j": 0.0, "row_id": float(row_id)}
from .research_metrics import (
    HardwareConstraint,
    HardwareObjectiveWeights,
    ResearchMetricBundle,
    build_metric_bundle,
    constraint_violations,
    energy_delay_product,
    objective_score,
    roofline_efficiency,
)

__all__ = [
    "HardwareProfiler",
    "HardwareTarget",
    "CortexM4",
    "EdgeTPU",
    "GenericGPU",
    "Quantizer",
    "quantization_error",
    "MemoryHierarchy",
    "Accelerator",
    "CycleAccurateHardwareModel",
    "MemoryController",
    "SimpleCPU",
    "SystolicArray",
    "EnergyModel",
    "TSMC28nmEnergy",
    "TSMC7nmEnergy",
    "calibration_table",
    "estimate_from_table",
    "HardwareConstraint",
    "HardwareObjectiveWeights",
    "ResearchMetricBundle",
    "build_metric_bundle",
    "constraint_violations",
    "energy_delay_product",
    "objective_score",
    "roofline_efficiency",
]
