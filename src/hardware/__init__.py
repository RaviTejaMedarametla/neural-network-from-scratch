"""Hardware exports."""

from .profiler import HardwareProfiler, HardwareTarget, CortexM4, EdgeTPU, GenericGPU
from .quantization import Quantizer, quantization_error
from .memory import MemoryHierarchy
from .accelerator import Accelerator
from .cycle_accurate import CycleAccurateHardwareModel, MemoryController, SimpleCPU, SystolicArray
from .energy_model import EnergyModel, TSMC28nmEnergy, TSMC7nmEnergy

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
]

from .research_tables import calibration_table, estimate_from_table

__all__.extend(["calibration_table", "estimate_from_table"])
