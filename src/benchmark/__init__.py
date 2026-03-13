"""Benchmark exports."""

from .hardware_bench import benchmark_on_hardware, pareto_frontier
from .compare_frameworks import compare_numpy_backends
from .research_suite import HardwareOptimizationStudy, StudyResult

__all__ = [
    "benchmark_on_hardware",
    "pareto_frontier",
    "compare_numpy_backends",
    "HardwareOptimizationStudy",
    "StudyResult",
]
