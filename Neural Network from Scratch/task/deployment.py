"""Deployment utilities: model export, validation and inference benchmarking."""
from __future__ import annotations
import time
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
from student import NeuralNetwork

def export_numpy_checkpoint(model: NeuralNetwork, output_path: str) -> Path:
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); model.save_weights(str(path)); return path

def _resolve_onnx_dependencies() -> Tuple[object, object, object]:
    try: import torch
    except ImportError as exc: raise RuntimeError("ONNX export requires torch. Install with `pip install torch`.") from exc
    try: import onnx
    except ImportError as exc: raise RuntimeError("ONNX export requires onnx. Install with `pip install onnx`.") from exc
    try: import onnxruntime as ort
    except ImportError as exc: raise RuntimeError("ONNX validation/inference requires onnxruntime. Install with `pip install onnxruntime`.") from exc
    return torch, onnx, ort

def validate_onnx_model(onnx_path: str) -> None:
    _, onnx, _ = _resolve_onnx_dependencies(); onnx.checker.check_model(onnx.load(onnx_path))

def run_onnx_inference(onnx_path: str, X: np.ndarray) -> np.ndarray:
    _, _, ort = _resolve_onnx_dependencies(); s = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    return s.run(None, {s.get_inputs()[0].name: X.astype(np.float32)})[0]

def export_onnx_from_pytorch(layer_sizes, activations, output_path: str, validate: bool = True) -> str:
    from pytorch_model import TorchNeuralNetwork, is_torch_available
    if not is_torch_available(): raise RuntimeError("Cannot export ONNX because torch is not installed")
    torch, _, _ = _resolve_onnx_dependencies()
    model = TorchNeuralNetwork(layer_sizes=layer_sizes, activations=activations, seed=42).model
    output = Path(output_path); output.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(model, torch.randn(1, layer_sizes[0], dtype=torch.float32), str(output), input_names=["input"], output_names=["output"], opset_version=13)
    if validate: validate_onnx_model(str(output))
    return str(output)

def run_inference(model: NeuralNetwork, X: np.ndarray, precision: str = "float32") -> np.ndarray: return model.forward(X, training=False, precision=precision)
def measure_inference_latency(model: NeuralNetwork, X: np.ndarray, precision: str = "float32", runs: int = 10) -> float:
    timings=[]
    for _ in range(runs): t0=time.perf_counter(); model.forward(X, training=False, precision=precision); timings.append(time.perf_counter()-t0)
    return float(np.mean(timings))/X.shape[0]
def batch_inference_throughput(model: NeuralNetwork, X: np.ndarray, precision: str = "float32", runs: int = 10) -> float:
    timings=[]
    for _ in range(runs): t0=time.perf_counter(); model.forward(X, training=False, precision=precision); timings.append(time.perf_counter()-t0)
    avg=float(np.mean(timings)); return X.shape[0]/avg if avg>0 else float("inf")
def inference_report(model: NeuralNetwork, X: np.ndarray, precision: str = "float32") -> Dict[str, float]:
    latency=measure_inference_latency(model,X,precision=precision); throughput=batch_inference_throughput(model,X,precision=precision)
    return {"precision": precision, "latency_per_sample_s": round(latency, 8), "throughput_samples_per_s": round(throughput, 3)}
