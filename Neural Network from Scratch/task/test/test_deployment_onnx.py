import importlib.util
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from deployment import export_onnx_from_pytorch, validate_onnx_export


def _is_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


@unittest.skipUnless(_is_available("onnx") and _is_available("onnxruntime"), "onnx and onnxruntime are required")
class DeploymentOnnxTests(unittest.TestCase):
    def test_export_and_runtime_output_match(self):
        layer_sizes = [784, 64, 10]
        activations = ["relu", "softmax"]
        export_path = PROJECT_ROOT / "exports" / "test_model.onnx"

        try:
            onnx_path = export_onnx_from_pytorch(layer_sizes, activations, str(export_path))
            self.assertTrue(Path(onnx_path).exists(), f"Expected ONNX file at {onnx_path}")

            matches, max_abs_diff = validate_onnx_export(layer_sizes, activations, onnx_path, seed=42)
            self.assertTrue(
                matches,
                f"ONNX and PyTorch outputs diverged beyond tolerance (max_abs_diff={max_abs_diff:.8f})",
            )
        finally:
            export_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
