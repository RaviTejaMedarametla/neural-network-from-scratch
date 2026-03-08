import unittest
import numpy as np
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.student import TwoLayerNeural


class VectorizedModelTests(unittest.TestCase):
    def test_forward_output_shape_and_probabilities(self):
        np.random.seed(7)
        x = np.random.randn(8, 6)
        model = TwoLayerNeural(n_features=6, n_classes=3, hidden_activation='relu', output_activation='softmax')

        preds = model.forward(x)

        self.assertEqual(preds.shape, (8, 3))
        np.testing.assert_allclose(np.sum(preds, axis=1), np.ones(8), atol=1e-7)

    def test_training_accuracy_not_degraded_on_synthetic_data(self):
        np.random.seed(11)
        n_samples = 400
        x = np.random.randn(n_samples, 2)
        y = ((x[:, 0] * x[:, 1]) > 0).astype(int)

        model = TwoLayerNeural(n_features=2, n_classes=2, hidden_activation='relu', output_activation='softmax')
        history = model.fit(x, y, epochs=120, alpha=0.2, batch_size=32, shuffle=True, seed=11)

        self.assertGreaterEqual(history['accuracy'][-1], 0.9)

    def test_inference_precision_modes(self):
        cfg = PrecisionConfig(train_dtype='float32', infer_precision='float16', seed=3)
        model = TwoLayerNeural(n_features=4, n_classes=3, hidden_activation='relu', output_activation='softmax',
                               precision_config=cfg)
        x = np.random.default_rng(5).normal(size=(10, 4)).astype(np.float32)
        y16 = model.forward(x, training=False, precision='float16')
        self.assertEqual(y16.dtype, np.float16)

        y8 = model.forward(x, training=False, precision='int8')
        self.assertEqual(y8.dtype, np.float32)
        self.assertEqual(y8.shape, (10, 3))
        np.testing.assert_allclose(np.sum(y8, axis=1), np.ones(10), atol=5e-2)

    def test_reproducible_training_with_seed(self):
        x = np.random.default_rng(21).normal(size=(120, 3)).astype(np.float32)
        y = (x[:, 0] + x[:, 1] > 0).astype(int)

        cfg1 = PrecisionConfig(seed=19)
        cfg2 = PrecisionConfig(seed=19)
        model_a = TwoLayerNeural(3, 2, hidden_activation='relu', output_activation='softmax', precision_config=cfg1)
        model_b = TwoLayerNeural(3, 2, hidden_activation='relu', output_activation='softmax', precision_config=cfg2)

        hist_a = model_a.fit(x, y, epochs=20, alpha=0.1, batch_size=16, seed=19)
        hist_b = model_b.fit(x, y, epochs=20, alpha=0.1, batch_size=16, seed=19)

        np.testing.assert_allclose(hist_a['loss'], hist_b['loss'], atol=1e-7)


if __name__ == '__main__':
    unittest.main()
