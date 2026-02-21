"""Inference-only CLI pipeline with optional ONNX export."""
from __future__ import annotations
import argparse, json, logging
import numpy as np
from config import PrecisionConfig
from deployment import export_onnx_from_pytorch, inference_report, run_onnx_inference
from reproducibility import set_global_seed
from student import NeuralNetwork
LOGGER = logging.getLogger(__name__)

def _load_npz_weights(model: NeuralNetwork, weights_path: str) -> None: model.load_weights(weights_path)

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    p=argparse.ArgumentParser(description="Run inference-only evaluation")
    p.add_argument("--weights", required=True); p.add_argument("--precision", default="float32", choices=["float32","float16","int8"])
    p.add_argument("--batch-size", type=int, default=64); p.add_argument("--export-onnx", action="store_true"); args=p.parse_args()
    set_global_seed(42); layer_sizes=[784,64,10]; activations=["relu","softmax"]
    model=NeuralNetwork(layer_sizes=layer_sizes, activations=activations, precision_config=PrecisionConfig(train_dtype="float32", infer_precision=args.precision, seed=42))
    _load_npz_weights(model,args.weights)
    X=np.random.default_rng(42).normal(size=(args.batch_size, layer_sizes[0])).astype(np.float32)
    print(json.dumps(inference_report(model, X, precision=args.precision), indent=2))
    if args.export_onnx:
        try:
            onnx_path=export_onnx_from_pytorch(layer_sizes, activations, "exports/model.onnx", validate=True)
            run_onnx_inference(onnx_path, X[:4]); LOGGER.info("Exported and validated ONNX model at %s", onnx_path)
        except (RuntimeError, ValueError, OSError) as exc:
            LOGGER.error("ONNX export failed: %s", exc); LOGGER.error("Install missing dependencies (torch, onnx, onnxruntime) and retry.")
            raise SystemExit(2) from exc
if __name__ == "__main__": main()
