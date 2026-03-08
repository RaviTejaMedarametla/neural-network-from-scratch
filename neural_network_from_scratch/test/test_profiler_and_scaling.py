import tempfile
import unittest
from pathlib import Path

import numpy as np

from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.profiler import profile_model
from neural_network_from_scratch.scaling_study import ScalingConfig, run_scaling_study
from neural_network_from_scratch.student import NeuralNetwork


class ProfilerAndScalingTests(unittest.TestCase):
    def test_profiler_generates_json_report(self):
        model = NeuralNetwork([8, 4, 2], ["relu", "softmax"], precision_config=PrecisionConfig(seed=1))
        with tempfile.TemporaryDirectory() as td:
            report, path = profile_model(model, batch_size=4, output_dir=td)
            self.assertTrue(path.exists())
            self.assertGreater(report["total_trainable_parameters"], 0)
            self.assertIn("activation_memory", report)

    def test_scaling_study_artifacts_created(self):
        cfg = ScalingConfig(
            dataset_sizes=[32],
            model_depths=[1],
            precision_modes=["float32"],
            epochs=1,
            input_dim=8,
            hidden_dim=16,
            n_classes=3,
        )
        with tempfile.TemporaryDirectory() as td:
            rows = run_scaling_study(cfg, output_dir=Path(td))
            self.assertEqual(len(rows), 1)
            self.assertTrue((Path(td) / "scaling_results.csv").exists())
            self.assertTrue((Path(td) / "summary_report.md").exists())


if __name__ == "__main__":
    unittest.main()
