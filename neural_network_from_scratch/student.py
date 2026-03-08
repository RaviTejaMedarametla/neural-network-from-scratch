"""Educational wrappers around the canonical NeuralNetwork implementation."""

import matplotlib.pyplot as plt
import numpy as np

from neural_network_from_scratch.config import DEFAULT_CONFIG
from neural_network_from_scratch.training import NeuralNetwork as CanonicalNeuralNetwork


class NeuralNetwork(CanonicalNeuralNetwork):
    """Educational alias for the canonical model class."""


class TwoLayerNeural(NeuralNetwork):
    def __init__(
        self,
        n_features,
        n_classes,
        hidden_activation="sigmoid",
        output_activation="sigmoid",
        l2_lambda=0.0,
        dropout_rate=0.0,
        precision_config=DEFAULT_CONFIG,
    ):
        super().__init__(
            [n_features, 64, n_classes],
            [hidden_activation, output_activation],
            l2_lambda=l2_lambda,
            dropout_rate=dropout_rate,
            precision_config=precision_config,
        )
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

    @property
    def weights1(self):
        return self.layers[0].weights

    @weights1.setter
    def weights1(self, value):
        self.layers[0].weights = value

    @property
    def bias1(self):
        return self.layers[0].bias

    @bias1.setter
    def bias1(self, value):
        self.layers[0].bias = value

    @property
    def weights2(self):
        return self.layers[1].weights

    @weights2.setter
    def weights2(self, value):
        self.layers[1].weights = value

    @property
    def bias2(self):
        return self.layers[1].bias

    @bias2.setter
    def bias2(self, value):
        self.layers[1].bias = value

    def forward(self, X, training=False, precision=None):
        out = super().forward(X, training=training, precision=precision)
        if self.layers[0].z_cache is not None and len(self.a_values) >= 2:
            self.Z1 = self.layers[0].z_cache
            self.A1 = self.a_values[0]
            self.Z2 = self.layers[1].z_cache
            self.A2 = self.a_values[1]
        return out


def plot_training(history):
    epochs = np.arange(1, len(history["loss"]) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(epochs, history["loss"])
    axes[0].set_title("Loss vs Epochs")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")

    axes[1].plot(epochs, history["accuracy"])
    axes[1].set_title("Accuracy vs Epochs")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")

    plt.tight_layout()
    plt.show()
