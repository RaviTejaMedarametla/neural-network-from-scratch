import tempfile
import unittest
from pathlib import Path

import numpy as np

from deployment import export_onnx_from_pytorch, run_onnx_inference
from student import NeuralNetwork


def _onnx_ready() -> bool:
    try:
        import onnx  # noqa: F401
        import onnxruntime  # noqa: F401
        return True
    except ImportError:
        return False

@unittest.skipUnless(_onnx_ready(), "onnx/onnxruntime are required for ONNX deployment tests")
class OnnxDeploymentTests(unittest.TestCase):
    def test_onnx_export_and_inference(self):
        model = NeuralNetwork([8, 4, 3], ["relu", "softmax"])
        with tempfile.TemporaryDirectory() as td:
            ckpt_path = Path(td) / "tiny.npz"
            model.save_weights(str(ckpt_path))
            onnx_path = Path(td) / "tiny.onnx"
            exported = export_onnx_from_pytorch([8, 4, 3], ["relu", "softmax"], str(onnx_path), validate=True)
            self.assertTrue(Path(exported).exists())

            x = np.random.default_rng(3).normal(size=(5, 8)).astype(np.float32)
            out = run_onnx_inference(str(onnx_path), x)
            self.assertEqual(out.shape, (5, 3))


if __name__ == "__main__":
    unittest.main()
