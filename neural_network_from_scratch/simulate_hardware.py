from datetime import datetime, timezone

import numpy as np

from neural_network_from_scratch.logging_utils import get_logger
from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.hardware_simulation import (
    config_from_precision_config,
    run_training_with_hardware_constraints,
    save_hardware_log,
)
from neural_network_from_scratch.student import NeuralNetwork

logger = get_logger(__name__)


def make_synthetic_data(n_samples=256, n_features=32, n_classes=4, seed=42):
    """Generate deterministic synthetic classification data."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n_samples, n_features)).astype(np.float32)
    y = rng.integers(0, n_classes, size=n_samples, dtype=np.int32)
    return X, y


def run_scenarios():
    """Run predefined hardware-constrained training scenarios."""
    X, y = make_synthetic_data()
    layer_sizes = [32, 64, 4]
    activations = ["relu", "softmax"]

    scenarios = [
        PrecisionConfig(
            enable_hardware_simulation=True,
            max_memory_mb=8.0,
            compute_speed_factor=1.0,
            precision_mode="float32",
            batch_size_limit=64,
        ),
        PrecisionConfig(
            enable_hardware_simulation=True,
            max_memory_mb=2.0,
            compute_speed_factor=1.5,
            precision_mode="float16",
            batch_size_limit=64,
        ),
        PrecisionConfig(
            enable_hardware_simulation=True,
            max_memory_mb=0.2,
            compute_speed_factor=2.0,
            precision_mode="int8",
            batch_size_limit=32,
        ),
    ]

    results = []
    for idx, precision_cfg in enumerate(scenarios, start=1):
        model = NeuralNetwork(layer_sizes=layer_sizes, activations=activations, precision_config=precision_cfg)
        simulation_cfg = config_from_precision_config(precision_cfg)

        outcome = run_training_with_hardware_constraints(
            model=model,
            X=X,
            y=y,
            epochs=2,
            alpha=0.1,
            batch_size=64,
            seed=42,
            simulation_config=simulation_cfg,
        )
        outcome["scenario"] = f"scenario_{idx}"
        results.append(outcome)

        logger.info("%s: %s", outcome["scenario"], outcome)

    log_file = save_hardware_log(
        {
            "simulation_config": None,
            "results": results,
        },
        output_dir="hardware_results",
        filename=f"simulation_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json",
    )
    logger.info("Saved hardware simulation log to: %s", log_file)


if __name__ == "__main__":
    run_scenarios()
