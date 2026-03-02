"""Deployment utilities: model export and inference benchmarking."""

from __future__ import annotations

import importlib.util
import time
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

from runtime_model import NeuralNetwork


def export_numpy_checkpoint(model: NeuralNetwork, output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    model.save_weights(str(path))
    return path


def export_onnx_from_pytorch(layer_sizes, activations, output_path: str) -> str:
    from pytorch_model import TorchNeuralNetwork, is_torch_available

    if not is_torch_available():
        raise RuntimeError("Cannot export ONNX because torch is not installed")
    if importlib.util.find_spec("onnx") is None:
        raise RuntimeError("Cannot export ONNX because onnx is not installed")

    import torch

    wrapper = TorchNeuralNetwork(layer_sizes=layer_sizes, activations=activations, seed=42)
    model = wrapper.model
    model = model.to(torch.device("cpu"))
    model.eval()

    dummy = torch.linspace(0.0, 1.0, steps=layer_sizes[0], dtype=torch.float32).reshape(1, layer_sizes[0])

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(
        model,
        dummy,
        str(output),
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
        opset_version=13,
    )
    return str(output)


def validate_onnx_export(layer_sizes, activations, onnx_path: str, seed: int = 42) -> Tuple[bool, float]:
    import onnxruntime as ort

    from pytorch_model import TorchNeuralNetwork

    rng = np.random.default_rng(seed)
    x = rng.normal(loc=0.0, scale=1.0, size=(3, layer_sizes[0])).astype(np.float32)

    torch_wrapper = TorchNeuralNetwork(layer_sizes=layer_sizes, activations=activations, seed=seed)
    torch_wrapper.model = torch_wrapper.model.to(torch_wrapper.device)
    torch_wrapper.model.eval()
    expected = torch_wrapper.forward(x, training=False, precision="float32")

    session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    actual = session.run(None, {input_name: x})[0]

    max_abs_diff = float(np.max(np.abs(expected - actual)))
    return bool(np.allclose(expected, actual, atol=1e-5, rtol=1e-4)), max_abs_diff


def run_inference(model: NeuralNetwork, X: np.ndarray, precision: str = "float32") -> np.ndarray:
    return model.forward(X, training=False, precision=precision)


def measure_inference_latency(model: NeuralNetwork, X: np.ndarray, precision: str = "float32", runs: int = 10) -> float:
    timings = []
    for _ in range(runs):
        t0 = time.perf_counter()
        model.forward(X, training=False, precision=precision)
        timings.append(time.perf_counter() - t0)
    return float(np.mean(timings)) / X.shape[0]


def batch_inference_throughput(model: NeuralNetwork, X: np.ndarray, precision: str = "float32", runs: int = 10) -> float:
    timings = []
    for _ in range(runs):
        t0 = time.perf_counter()
        model.forward(X, training=False, precision=precision)
        timings.append(time.perf_counter() - t0)
    avg = float(np.mean(timings))
    return X.shape[0] / avg if avg > 0 else float("inf")


def inference_report(model: NeuralNetwork, X: np.ndarray, precision: str = "float32") -> Dict[str, float]:
    latency = measure_inference_latency(model, X, precision=precision)
    throughput = batch_inference_throughput(model, X, precision=precision)
    return {
        "precision": precision,
        "latency_per_sample_s": round(latency, 8),
        "throughput_samples_per_s": round(throughput, 3),
    }
