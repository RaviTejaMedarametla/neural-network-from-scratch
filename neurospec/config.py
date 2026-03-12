from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(slots=True)
class ModelConfig:
    """Configuration for MLP model built from scratch."""

    input_dim: int = 32
    hidden_dims: list[int] = field(default_factory=lambda: [64, 64, 32])
    output_dim: int = 10
    activation: Literal["relu", "gelu", "tanh"] = "gelu"
    weight_init: Literal["xavier", "he", "normal"] = "he"
    dropout: float = 0.05
    layer_norm: bool = True


@dataclass(slots=True)
class TrainingConfig:
    """Training settings."""

    learning_rate: float = 1e-2
    optimizer: Literal["sgd", "adam"] = "adam"
    batch_size: int = 128
    epochs: int = 25
    seed: int = 7
    weight_decay: float = 1e-4
    grad_clip_norm: float = 1.0
    label_smoothing: float = 0.05
    train_samples: int = 16_384
    val_samples: int = 4_096


@dataclass(slots=True)
class HardwareConfig:
    """Hardware design-space assumptions for accelerator simulation."""

    process_node_nm: int = 5
    frequency_ghz: float = 1.6
    voltage_v: float = 0.78
    sram_kb: int = 512
    hbm_bandwidth_gbps: float = 900.0
    mac_units: int = 4096
    noc_topology: Literal["mesh", "torus", "crossbar"] = "mesh"
    precision_bits: Literal[4, 8, 16, 32] = 8
    sparsity_support: bool = True
    utilization_target: float = 0.72
    tdp_watts: float = 280.0


@dataclass(slots=True)
class ExperimentConfig:
    """Top-level experiment configuration."""

    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    hardware: HardwareConfig = field(default_factory=HardwareConfig)
    study_name: str = "hardware_aware_nn"
    notes: str = (
        "A synthetic but research-structured study focusing on model quality, "
        "throughput, energy, latency, and memory efficiency."
    )
