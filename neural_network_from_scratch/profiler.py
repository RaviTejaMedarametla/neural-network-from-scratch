import argparse
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import numpy as np


BYTES_PER_DTYPE = {
    "float32": 4,
    "float16": 2,
    "int8": 1,
}


def _to_serializable(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_serializable(v) for v in value]
    return value


def _load_config_module(config_path: str):
    config_file = Path(config_path).resolve()
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    spec = importlib.util.spec_from_file_location("profiling_config", config_file)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import config from: {config_file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_model_from_config(config_module):
    if hasattr(config_module, "build_model") and callable(config_module.build_model):
        return config_module.build_model()

    if hasattr(config_module, "MODEL_INSTANCE"):
        return config_module.MODEL_INSTANCE

    if hasattr(config_module, "MODEL_CLASS"):
        model_class = config_module.MODEL_CLASS
        model_kwargs = getattr(config_module, "MODEL_KWARGS", {})
        return model_class(**model_kwargs)

    if hasattr(config_module, "LAYER_SIZES") and hasattr(config_module, "ACTIVATIONS"):
        from neural_network_from_scratch.student import NeuralNetwork

        return NeuralNetwork(
            layer_sizes=list(config_module.LAYER_SIZES),
            activations=list(config_module.ACTIVATIONS),
            precision_config=getattr(config_module, "DEFAULT_CONFIG", None),
        )

    raise ValueError(
        "Cannot construct model from config. Provide one of: "
        "build_model(), MODEL_INSTANCE, MODEL_CLASS+MODEL_KWARGS, or LAYER_SIZES+ACTIVATIONS."
    )


def _layer_param_counts(model) -> List[Dict[str, Any]]:
    layer_rows = []
    for idx, layer in enumerate(getattr(model, "layers", []), start=1):
        weights = getattr(layer, "weights", None)
        bias = getattr(layer, "bias", None)

        w_count = int(np.prod(weights.shape)) if weights is not None else 0
        b_count = int(np.prod(bias.shape)) if bias is not None else 0
        layer_rows.append(
            {
                "layer": f"layer_{idx}",
                "type": layer.__class__.__name__,
                "weights": w_count,
                "bias": b_count,
                "total": w_count + b_count,
                "weights_shape": list(weights.shape) if weights is not None else [],
                "bias_shape": list(bias.shape) if bias is not None else [],
            }
        )
    return layer_rows


def _activation_memory_bytes(model, input_shape):
    x = np.zeros(input_shape, dtype=np.float32)
    model.forward(x, training=False, precision="float32")

    total_bytes = int(x.nbytes)
    details = [{"tensor": "input", "shape": list(x.shape), "bytes": int(x.nbytes)}]

    for idx, activation in enumerate(getattr(model, "a_values", []), start=1):
        bytes_count = int(np.asarray(activation).nbytes)
        details.append({
            "tensor": f"activation_{idx}",
            "shape": list(np.asarray(activation).shape),
            "bytes": bytes_count,
        })
        total_bytes += bytes_count

    return total_bytes, details


def profile_model(model, batch_size=1, output_dir="profiling"):
    if not hasattr(model, "layer_sizes"):
        raise ValueError("Model must expose layer_sizes for dynamic profiling.")

    input_shape = (int(batch_size), int(model.layer_sizes[0]))
    layers = _layer_param_counts(model)
    total_params = int(sum(layer["total"] for layer in layers))

    memory_footprint_mb = {
        dtype: round((total_params * byte_size) / (1024 ** 2), 6)
        for dtype, byte_size in BYTES_PER_DTYPE.items()
    }

    act_bytes, act_details = _activation_memory_bytes(model, input_shape)

    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model": model.__class__.__name__,
        "layer_sizes": list(getattr(model, "layer_sizes", [])),
        "batch_size": int(batch_size),
        "total_trainable_parameters": total_params,
        "layer_wise_parameters": layers,
        "parameter_memory_mb": memory_footprint_mb,
        "activation_memory": {
            "bytes": int(act_bytes),
            "mb": round(act_bytes / (1024 ** 2), 6),
            "details": act_details,
        },
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    report_file = output_path / f"profile_{model.__class__.__name__.lower()}.json"
    report_file.write_text(json.dumps(_to_serializable(report), indent=2), encoding="utf-8")

    return report, report_file


def summary_table(report: Dict[str, Any]) -> str:
    lines = [
        "\nModel Profiling Summary",
        "=" * 72,
        f"Model: {report['model']}",
        f"Layer sizes: {report['layer_sizes']}",
        f"Total trainable parameters: {report['total_trainable_parameters']}",
        "",
        "Layer-wise parameters:",
        f"{'Layer':<12}{'Type':<16}{'Weights':>12}{'Bias':>12}{'Total':>12}",
        "-" * 72,
    ]

    for row in report["layer_wise_parameters"]:
        lines.append(
            f"{row['layer']:<12}{row['type']:<16}{row['weights']:>12,}{row['bias']:>12,}{row['total']:>12,}"
        )

    lines.extend(
        [
            "",
            "Parameter memory footprint (MB):",
            f"  float32: {report['parameter_memory_mb']['float32']}",
            f"  float16: {report['parameter_memory_mb']['float16']}",
            f"  int8:    {report['parameter_memory_mb']['int8']}",
            "",
            "Activation memory estimate:",
            f"  bytes: {report['activation_memory']['bytes']}",
            f"  mb:    {report['activation_memory']['mb']}",
        ]
    )

    return "\n".join(lines)


def run_from_config(config_path: str):
    config_module = _load_config_module(config_path)
    model = _build_model_from_config(config_module)

    batch_size = int(getattr(config_module, "PROFILE_BATCH_SIZE", 1))
    output_dir = getattr(config_module, "PROFILE_OUTPUT_DIR", "profiling")

    report, output_file = profile_model(model=model, batch_size=batch_size, output_dir=output_dir)
    print(summary_table(report))
    print(f"\nSaved profiling report to: {output_file}")
    return report, output_file


def main():
    parser = argparse.ArgumentParser(description="Profile a neural network architecture from config.")
    parser.add_argument("--config", required=True, help="Path to a Python config module (e.g., config.py).")
    args = parser.parse_args()
    run_from_config(args.config)


if __name__ == "__main__":
    main()
