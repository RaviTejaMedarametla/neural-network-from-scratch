import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

import numpy as np


DTYPE_BYTES = {
    "float32": 4,
    "float16": 2,
    "int8": 1,
}


@dataclass
class HardwareSimulationConfig:
    enabled: bool = False
    max_memory_mb: float = 512.0
    compute_speed_factor: float = 1.0
    precision_mode: str = "float32"  # float32 | float16 | int8
    batch_size_limit: int = 128


class HardwareConstraintWarning(UserWarning):
    pass


def _dtype_bytes(precision_mode: str) -> int:
    return DTYPE_BYTES.get(precision_mode, DTYPE_BYTES["float32"])


def _layer_param_count(layer: Any) -> int:
    weights = getattr(layer, "weights", None)
    bias = getattr(layer, "bias", None)
    w_count = int(np.prod(weights.shape)) if weights is not None else 0
    b_count = int(np.prod(bias.shape)) if bias is not None else 0
    return w_count + b_count


def estimate_parameter_memory_mb(model: Any, precision_mode: str = "float32") -> float:
    total_params = sum(_layer_param_count(layer) for layer in getattr(model, "layers", []))
    return (total_params * _dtype_bytes(precision_mode)) / (1024 ** 2)


def estimate_activation_memory_mb(model: Any, batch_size: int, precision_mode: str = "float32") -> float:
    if not hasattr(model, "layer_sizes"):
        return 0.0

    dtype_bytes = _dtype_bytes(precision_mode)
    activation_elements = 0

    # input + each layer output
    for width in model.layer_sizes:
        activation_elements += int(batch_size) * int(width)

    return (activation_elements * dtype_bytes) / (1024 ** 2)


def estimate_total_memory_mb(model: Any, batch_size: int, precision_mode: str = "float32") -> float:
    return estimate_parameter_memory_mb(model, precision_mode) + estimate_activation_memory_mb(
        model, batch_size, precision_mode
    )


def adjust_batch_size_to_memory(
    model: Any,
    requested_batch_size: int,
    max_memory_mb: float,
    precision_mode: str = "float32",
    batch_size_limit: int = 128,
) -> int:
    capped_batch = max(1, min(int(requested_batch_size), int(batch_size_limit)))

    if estimate_total_memory_mb(model, capped_batch, precision_mode) <= max_memory_mb:
        return capped_batch

    low, high = 1, capped_batch
    feasible = 0

    while low <= high:
        mid = (low + high) // 2
        memory = estimate_total_memory_mb(model, mid, precision_mode)
        if memory <= max_memory_mb:
            feasible = mid
            low = mid + 1
        else:
            high = mid - 1

    return feasible


def apply_precision_constraint(model: Any, precision_mode: str) -> None:
    if hasattr(model, "infer_precision"):
        model.infer_precision = precision_mode


def apply_compute_slowdown(elapsed_seconds: float, compute_speed_factor: float) -> float:
    if compute_speed_factor <= 1.0:
        return 0.0

    delay = elapsed_seconds * (compute_speed_factor - 1.0)
    time.sleep(delay)
    return delay


def prepare_hardware_constrained_run(
    model: Any,
    requested_batch_size: int,
    simulation_config: HardwareSimulationConfig,
) -> Dict[str, Any]:
    if not simulation_config.enabled:
        return {
            "enabled": False,
            "batch_size": requested_batch_size,
            "warnings": [],
        }

    warnings: List[str] = []
    precision = simulation_config.precision_mode
    adjusted_batch_size = adjust_batch_size_to_memory(
        model=model,
        requested_batch_size=requested_batch_size,
        max_memory_mb=simulation_config.max_memory_mb,
        precision_mode=precision,
        batch_size_limit=simulation_config.batch_size_limit,
    )

    if adjusted_batch_size == 0:
        warnings.append(
            "Model cannot run under current memory and precision constraints; even batch_size=1 exceeds max_memory_mb."
        )
        adjusted_batch_size = 1

    projected_memory = estimate_total_memory_mb(model, adjusted_batch_size, precision)

    if projected_memory > simulation_config.max_memory_mb:
        warnings.append(
            f"Projected memory ({projected_memory:.4f} MB) exceeds limit ({simulation_config.max_memory_mb:.4f} MB)."
        )

    if adjusted_batch_size < requested_batch_size:
        warnings.append(
            f"Batch size reduced from {requested_batch_size} to {adjusted_batch_size} due to memory constraints."
        )

    apply_precision_constraint(model, precision)

    return {
        "enabled": True,
        "batch_size": adjusted_batch_size,
        "precision_mode": precision,
        "estimated_memory_mb": round(projected_memory, 6),
        "warnings": warnings,
    }


def run_training_with_hardware_constraints(
    model: Any,
    X,
    y,
    epochs: int,
    alpha: float,
    batch_size: int,
    seed: int,
    simulation_config: HardwareSimulationConfig,
) -> Dict[str, Any]:
    setup = prepare_hardware_constrained_run(model, batch_size, simulation_config)
    effective_batch_size = int(setup["batch_size"])

    start = time.perf_counter()
    history = model.fit(
        X,
        y,
        epochs=epochs,
        alpha=alpha,
        batch_size=effective_batch_size,
        seed=seed,
    )
    elapsed = time.perf_counter() - start
    added_delay = apply_compute_slowdown(elapsed, simulation_config.compute_speed_factor)

    result = {
        "setup": setup,
        "training_time_s": round(elapsed, 6),
        "artificial_delay_s": round(added_delay, 6),
        "effective_time_s": round(elapsed + added_delay, 6),
        "final_accuracy": round(float(history["accuracy"][-1]), 6),
        "final_loss": round(float(history["loss"][-1]), 6),
    }
    return result


def config_from_precision_config(precision_config: Any) -> HardwareSimulationConfig:
    return HardwareSimulationConfig(
        enabled=bool(getattr(precision_config, "enable_hardware_simulation", False)),
        max_memory_mb=float(getattr(precision_config, "max_memory_mb", 512.0)),
        compute_speed_factor=float(getattr(precision_config, "compute_speed_factor", 1.0)),
        precision_mode=str(getattr(precision_config, "precision_mode", "float32")),
        batch_size_limit=int(getattr(precision_config, "batch_size_limit", 128)),
    )


def save_hardware_log(log_payload: Dict[str, Any], output_dir: str = "hardware_results", filename: str = "run_log.json"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    payload = {
        "config": asdict(log_payload["simulation_config"])
        if isinstance(log_payload.get("simulation_config"), HardwareSimulationConfig)
        else log_payload.get("simulation_config"),
        "results": log_payload.get("results", []),
    }
    destination = output_path / filename
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return destination
