from dataclasses import dataclass

from dataset_config import FASHION_MNIST_SPEC


@dataclass
class PrecisionConfig:
    train_dtype: str = "float32"
    infer_precision: str = "float32"  # float32 | float16 | int8
    int8_clip_value: int = 127
    seed: int = 42
    enable_profiling: bool = False
    enable_hardware_simulation: bool = False
    max_memory_mb: float = 512.0
    compute_speed_factor: float = 1.0
    precision_mode: str = "float32"
    batch_size_limit: int = 128


DEFAULT_CONFIG = PrecisionConfig()

# Profiling defaults used by profiler.py CLI
LAYER_SIZES = [784, 64, 10]
ACTIVATIONS = ["relu", "softmax"]
PROFILE_BATCH_SIZE = 32
PROFILE_OUTPUT_DIR = "profiling"


def build_model():
    from runtime_model import NeuralNetwork

    return NeuralNetwork(
        layer_sizes=LAYER_SIZES,
        activations=ACTIVATIONS,
        precision_config=DEFAULT_CONFIG,
    )


EXPERIMENT_CONFIGS = {
    "baseline": {
        "dataset_version": "synthetic-v1",
        "layer_sizes": [784, 64, 10],
        "activations": ["relu", "softmax"],
        "epochs": 2,
        "alpha": 0.1,
        "batch_size": 32,
        "seed": 42,
        "precision": "float32",
        "hardware_constraint_mode": "off",
        "synthetic_mode": True,
        "synthetic_samples": 512,
    },
    "real_fashion_mnist": {
        "dataset_path": FASHION_MNIST_SPEC.train_path,
        "dataset_version": FASHION_MNIST_SPEC.version,
        "layer_sizes": [784, 64, 10],
        "activations": ["relu", "softmax"],
        "epochs": 3,
        "alpha": 0.1,
        "batch_size": 32,
        "seed": 42,
        "precision": "float32",
        "hardware_constraint_mode": "off",
        "synthetic_mode": False,
        "dataset_min_rows": 100,
        "dataset_auto_prepare": True,
        "dataset_sha256": None,
    },
    "synthetic_baseline": {
        "dataset_version": "synthetic-v1",
        "layer_sizes": [784, 64, 10],
        "activations": ["relu", "softmax"],
        "epochs": 2,
        "alpha": 0.1,
        "batch_size": 32,
        "seed": 42,
        "precision": "float32",
        "hardware_constraint_mode": "off",
        "synthetic_mode": True,
        "synthetic_samples": 512,
        "dataset_auto_prepare": False,
    },
}
