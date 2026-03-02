import tempfile
import unittest
from pathlib import Path

import numpy as np

from experiment_manager import ExperimentManager
from hardware_simulation import HardwareSimulationConfig, prepare_hardware_constrained_run
from runtime_model import NeuralNetwork


class HardwareAndExperimentManagerTests(unittest.TestCase):
    def test_hardware_batch_adjustment(self):
        model = NeuralNetwork([16, 32, 4], ["relu", "softmax"])
        cfg = HardwareSimulationConfig(
            enabled=True,
            max_memory_mb=0.01,
            precision_mode="float32",
            batch_size_limit=64,
        )
        setup = prepare_hardware_constrained_run(model, requested_batch_size=64, simulation_config=cfg)
        self.assertLessEqual(setup["batch_size"], 64)
        self.assertTrue(setup["enabled"])

    def test_experiment_manager_versioning_and_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            manager = ExperimentManager(log_dir=td)
            rec1 = manager.start_experiment(
                config_name="cfg",
                hyperparameters={"lr": 0.1},
                metadata={"precision": "float32", "model_size": "8x4", "dataset_version": "v1", "hardware_constraint_mode": "off"},
            )
            manager.log_metrics({"loss": [np.float32(0.1)]})
            manager.add_checkpoint("ckpt1.npz")

            rec2 = manager.start_experiment(
                config_name="cfg",
                hyperparameters={"lr": 0.2},
                metadata={"precision": "float32", "model_size": "8x4", "dataset_version": "v1", "hardware_constraint_mode": "off"},
            )
            self.assertEqual(rec1.version + 1, rec2.version)
            history = manager.read_history(rec1.experiment_id)
            self.assertEqual(len(history), 2)
            self.assertEqual(history[0]["checkpoints"], ["ckpt1.npz"])


if __name__ == "__main__":
    unittest.main()
