"""Hardware exports."""

from .profiler import HardwareProfiler, CortexM4, EdgeTPU, GenericGPU
from .quantization import Quantizer, quantization_error
from .memory import MemoryHierarchy
from .accelerator import Accelerator
from .cycle_accurate import CycleAccurateHardwareModel, MemoryController, SimpleCPU, SystolicArray
from .energy_model import EnergyModel, TSMC28nmEnergy, TSMC7nmEnergy
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
from .design_utils import estimate_from_table, calibration_table

__all__ = [
    "HardwareProfiler", "CortexM4", "EdgeTPU", "GenericGPU",
    "Quantizer", "quantization_error",
    "MemoryHierarchy",
    "Accelerator",
    "CycleAccurateHardwareModel", "MemoryController", "SimpleCPU", "SystolicArray",
    "EnergyModel", "TSMC28nmEnergy", "TSMC7nmEnergy",
    "HardwareConstraint", "HardwareObjectiveWeights", "ResearchMetricBundle",
    "build_metric_bundle", "constraint_violations", "energy_delay_product",
    "objective_score", "roofline_efficiency",
    "estimate_from_table", "calibration_table",
]
