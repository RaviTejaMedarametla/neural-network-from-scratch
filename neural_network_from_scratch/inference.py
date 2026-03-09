"""Inference-only CLI pipeline with optional ONNX export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from neural_network_from_scratch.logging_utils import get_logger
from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.deployment import export_onnx_from_pytorch, inference_report
from neural_network_from_scratch.reproducibility import set_global_seed
from neural_network_from_scratch.student import NeuralNetwork

logger = get_logger(__name__)


def _load_npz_weights(model: NeuralNetwork, weights_path: str) -> None:
    """Load serialized NumPy checkpoint weights into the model."""
    model.load_weights(weights_path)


def main() -> None:
    """CLI entrypoint for inference and optional ONNX export."""
    parser = argparse.ArgumentParser(description="Run inference-only evaluation")
    parser.add_argument("--weights", required=True, help="Path to .npz checkpoint")
    parser.add_argument("--precision", default="float32", choices=["float32", "float16", "int8"])
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--export-onnx", action="store_true")
    args = parser.parse_args()

    set_global_seed(42)
    layer_sizes = [784, 64, 10]
    activations = ["relu", "softmax"]
    cfg = PrecisionConfig(train_dtype="float32", infer_precision=args.precision, seed=42)
    model = NeuralNetwork(layer_sizes=layer_sizes, activations=activations, precision_config=cfg)

    _load_npz_weights(model, args.weights)

    X = np.random.default_rng(42).normal(size=(args.batch_size, layer_sizes[0])).astype(np.float32)
    report = inference_report(model, X, precision=args.precision)
    logger.info("Inference report:
%s", json.dumps(report, indent=2))

    if args.export_onnx:
        onnx_path = export_onnx_from_pytorch(layer_sizes, activations, "exports/model.onnx")
        logger.info("Exported ONNX model to %s", onnx_path)


if __name__ == "__main__":
    main()
