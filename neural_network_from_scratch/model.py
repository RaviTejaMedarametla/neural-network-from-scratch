"""Reference NumPy MLP implementation.

This module keeps a compact educational implementation that is independent from
higher-level training abstractions used in the rest of the package.
"""

from __future__ import annotations

import numpy as np


class NeuralNetwork:
    """Multi-layer perceptron with ReLU hidden layers and softmax output."""

    def __init__(self, layer_sizes, learning_rate=0.01, seed=42):
        if len(layer_sizes) < 2:
            raise ValueError("layer_sizes must include input and output dimensions")

        self.layer_sizes = list(layer_sizes)
        self.learning_rate = float(learning_rate)
        self.rng = np.random.default_rng(int(seed))

        self.weights = []
        self.biases = []
        for fan_in, fan_out in zip(self.layer_sizes[:-1], self.layer_sizes[1:]):
            weight = self.rng.standard_normal((fan_in, fan_out)) * np.sqrt(2.0 / fan_in)
            bias = np.zeros((1, fan_out), dtype=np.float64)
            self.weights.append(weight)
            self.biases.append(bias)

        self.cache = {}

    @staticmethod
    def _relu(x):
        return np.maximum(0.0, x)

    @staticmethod
    def _relu_derivative(x):
        return (x > 0.0).astype(np.float64)

    @staticmethod
    def _softmax(x):
        shifted = x - np.max(x, axis=1, keepdims=True)
        exp_x = np.exp(shifted)
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, X):
        self.cache = {"a0": X}
        activations = X

        for idx, (weight, bias) in enumerate(zip(self.weights, self.biases), start=1):
            z = activations @ weight + bias
            if idx < len(self.weights):
                activations = self._relu(z)
            else:
                activations = z
            self.cache[f"z{idx}"] = z
            self.cache[f"a{idx}"] = activations

        return self._softmax(activations)

    def backward(self, X, y, probs):
        batch_size = X.shape[0]

        delta = probs.copy()
        delta[np.arange(batch_size), y] -= 1.0
        delta /= batch_size

        grads_w = [None] * len(self.weights)
        grads_b = [None] * len(self.biases)

        for layer_idx in reversed(range(len(self.weights))):
            a_prev = self.cache[f"a{layer_idx}"]
            grads_w[layer_idx] = a_prev.T @ delta
            grads_b[layer_idx] = np.sum(delta, axis=0, keepdims=True)

            if layer_idx > 0:
                prev_z = self.cache[f"z{layer_idx}"]
                delta = (delta @ self.weights[layer_idx].T) * self._relu_derivative(prev_z)

        return grads_w, grads_b

    def update(self, grads_w, grads_b):
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * grads_w[i]
            self.biases[i] -= self.learning_rate * grads_b[i]

    def train_step(self, X_batch, y_batch):
        probs = self.forward(X_batch)
        grads_w, grads_b = self.backward(X_batch, y_batch, probs)
        self.update(grads_w, grads_b)
        return self._cross_entropy_loss(probs, y_batch)

    @staticmethod
    def _cross_entropy_loss(probs, y):
        m = y.shape[0]
        return float(np.mean(-np.log(probs[np.arange(m), y] + 1e-8)))

    def predict(self, X):
        return np.argmax(self.forward(X), axis=1)

    def accuracy(self, X, y):
        return float(np.mean(self.predict(X) == y))


NeuralNetworkModel = NeuralNetwork
