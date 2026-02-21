import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from train import run_experiment


class RealDatasetPipelineTests(unittest.TestCase):
    def test_real_dataset_experiment_runs_with_present_data(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            dataset_path = td_path / "fashion-mnist_train.csv"

            rng = np.random.default_rng(9)
            X = rng.integers(0, 255, size=(120, 784), dtype=np.int32)
            y = rng.integers(0, 10, size=(120, 1), dtype=np.int32)
            arr = np.hstack([y, X])
            header = ",".join(["label"] + [f"pixel{i}" for i in range(1, 785)])
            np.savetxt(dataset_path, arr, fmt="%d", delimiter=",", header=header, comments="")

            cfg = {
                "dataset_path": str(dataset_path),
                "dataset_version": "offline-test-v1",
                "layer_sizes": [784, 32, 10],
                "activations": ["relu", "softmax"],
                "epochs": 1,
                "alpha": 0.1,
                "batch_size": 16,
                "seed": 42,
                "precision": "float32",
                "hardware_constraint_mode": "off",
                "synthetic_mode": False,
                "dataset_min_rows": 100,
                "dataset_auto_prepare": False,
                "dataset_sha256": None,
            }
            cfg_path = td_path / "cfg.json"
            cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

            run_experiment(str(cfg_path))


if __name__ == "__main__":
    unittest.main()
