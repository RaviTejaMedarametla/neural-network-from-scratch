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
        if any(int(size) < 1 for size in layer_sizes):
            raise ValueError("all layer_sizes entries must be >= 1")

        self.layer_sizes = [int(size) for size in layer_sizes]
        self.learning_rate = float(learning_rate)
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be > 0")

        self.seed = int(seed)
        self.rng = np.random.default_rng(self.seed)

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

    def _validate_features(self, X, *, allow_empty: bool = False) -> np.ndarray:
        x = np.asarray(X, dtype=np.float64)
        if x.ndim != 2:
            raise ValueError("X must be a 2D array of shape (n_samples, n_features)")
        if not allow_empty and x.shape[0] < 1:
            raise ValueError("X must include at least one sample")
        if x.shape[1] != self.layer_sizes[0]:
            raise ValueError(f"X has {x.shape[1]} features but model expects {self.layer_sizes[0]}")
        if not np.all(np.isfinite(x)):
            raise ValueError("X must contain only finite values")
        return x

    def _validate_labels(self, y, n_samples: int) -> np.ndarray:
        labels = np.asarray(y, dtype=np.int64)
        if labels.ndim != 1:
            raise ValueError("y must be a 1D integer label array")
        if labels.shape[0] != n_samples:
            raise ValueError("X and y must contain the same number of samples")
        n_classes = self.layer_sizes[-1]
        if np.any(labels < 0) or np.any(labels >= n_classes):
            raise ValueError(f"y values must be in [0, {n_classes - 1}]")
        return labels

    def forward(self, X, training: bool | None = None, precision: str | None = None):
        del training, precision  # Compatibility with higher-level APIs.
        features = self._validate_features(X)

        self.cache = {"a0": features}
        activations = features

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
        features = self._validate_features(X)
        labels = self._validate_labels(y, n_samples=features.shape[0])
        probs = np.asarray(probs, dtype=np.float64)

        if probs.shape != (features.shape[0], self.layer_sizes[-1]):
            raise ValueError("probs must have shape (n_samples, n_classes)")

        batch_size = features.shape[0]
        delta = probs.copy()
        delta[np.arange(batch_size), labels] -= 1.0
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
        features = self._validate_features(X_batch)
        labels = self._validate_labels(y_batch, n_samples=features.shape[0])
        probs = self.forward(features)
        grads_w, grads_b = self.backward(features, labels, probs)
        self.update(grads_w, grads_b)
        return self._cross_entropy_loss(probs, labels)

    @staticmethod
    def _cross_entropy_loss(probs, y):
        m = y.shape[0]
        return float(np.mean(-np.log(probs[np.arange(m), y] + 1e-8)))

    def fit(self, X, y, epochs=10, batch_size=32, shuffle=True, seed=None):
        features = self._validate_features(X)
        labels = self._validate_labels(y, n_samples=features.shape[0])

        if int(epochs) < 1:
            raise ValueError("epochs must be >= 1")
        if int(batch_size) < 1:
            raise ValueError("batch_size must be >= 1")

        train_rng = np.random.default_rng(self.seed if seed is None else int(seed))
        n_samples = features.shape[0]
        history = {"loss": []}

        for _ in range(int(epochs)):
            indices = train_rng.permutation(n_samples) if shuffle else np.arange(n_samples)
            x_epoch = features[indices]
            y_epoch = labels[indices]

            epoch_loss = 0.0
            for start in range(0, n_samples, int(batch_size)):
                x_batch = x_epoch[start : start + int(batch_size)]
                y_batch = y_epoch[start : start + int(batch_size)]
                epoch_loss += self.train_step(x_batch, y_batch) * len(x_batch)
            history["loss"].append(float(epoch_loss / n_samples))

        return history


    def evaluate(self, X, y):
        features = self._validate_features(X)
        labels = self._validate_labels(y, n_samples=features.shape[0])
        probs = self.forward(features)
        return {
            "loss": self._cross_entropy_loss(probs, labels),
            "accuracy": float(np.mean(np.argmax(probs, axis=1) == labels)),
        }

    def predict(self, X, precision: str | None = None):
        del precision  # Compatibility with higher-level APIs.
        return np.argmax(self.forward(X), axis=1)

    def accuracy(self, X, y):
        labels = self._validate_labels(y, n_samples=self._validate_features(X).shape[0])
        return float(np.mean(self.predict(X) == labels))


NeuralNetworkModel = NeuralNetwork
