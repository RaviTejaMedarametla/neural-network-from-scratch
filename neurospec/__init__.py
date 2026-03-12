"""neurospec package."""

from .config import ExperimentConfig, HardwareConfig, ModelConfig, TrainingConfig
from .experiments import run_research_experiment

__all__ = [
    "ExperimentConfig",
    "HardwareConfig",
    "ModelConfig",
    "TrainingConfig",
    "run_research_experiment",
]
