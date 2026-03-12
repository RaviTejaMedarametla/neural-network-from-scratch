import unittest
import numpy as np

from neural_network_from_scratch import NeuralNetwork


class ModelTests(unittest.TestCase):
    def test_forward_shape(self):
        x = np.random.default_rng(0).normal(size=(5, 4))
        m = NeuralNetwork(n_features=4, seed=1)
        y = m.forward(x)
        self.assertEqual(y.shape, (5, 1))

    def test_input_validation(self):
        m = NeuralNetwork(n_features=3, seed=1)
        with self.assertRaises(ValueError):
            m.forward(np.ones((2, 2)))


if __name__ == '__main__':
    unittest.main()
