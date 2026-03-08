"""Core neural network forward/backward implementation."""

from __future__ import annotations

import numpy as np

from neural_network_from_scratch.activations import activation_backward, activation_forward
from neural_network_from_scratch.config import DEFAULT_CONFIG
from neural_network_from_scratch.layers import DenseLayer
from neural_network_from_scratch.loss import MeanSquaredError
from neural_network_from_scratch.precision import PrecisionMixin


class NeuralNetworkCore(PrecisionMixin):
    def __init__(self, layer_sizes, activations, l2_lambda=0.0, dropout_rate=0.0, precision_config=None):
        if len(layer_sizes) < 2:
            raise ValueError("layer_sizes must include input and output sizes")
        if len(activations) != len(layer_sizes) - 1:
            raise ValueError("activations must match number of layers minus one")

        self.config = DEFAULT_CONFIG if precision_config is None else precision_config
        self.train_dtype = np.dtype(self.config.train_dtype)
        self.infer_precision = self.config.infer_precision
        self.int8_clip_value = int(self.config.int8_clip_value)
        self.seed = int(self.config.seed)

        self.layer_sizes = list(layer_sizes)
        self.activations = list(activations)
        self.l2_lambda = l2_lambda
        self.dropout_rate = dropout_rate

        self.rng = np.random.default_rng(self.seed)
        self.layers = [
            DenseLayer(self.layer_sizes[i], self.layer_sizes[i + 1], rng=self.rng, dtype=self.train_dtype)
            for i in range(len(self.layer_sizes) - 1)
        ]
        self.a_values = []
        self.a_raw_values = []
        self.dropout_masks = []

    @property
    def weights(self):
        return [layer.weights for layer in self.layers]

    @property
    def biases(self):
        return [layer.bias for layer in self.layers]

    def set_seed(self, seed):
        self.seed = int(seed)
        self.rng = np.random.default_rng(self.seed)

    def _forward_with_precision(self, x, precision):
        current = x
        for layer, activation_name in zip(self.layers, self.activations):
            if precision == "int8":
                q_a, a_scale = self._quantize_to_int8(current)
                q_w, w_scale = self._quantize_to_int8(layer.weights)
                a_deq = self._dequantize_from_int8(q_a, a_scale)
                w_deq = self._dequantize_from_int8(q_w, w_scale)
                z = a_deq @ w_deq + layer.bias.astype(np.float32)
                z_q, z_scale = self._quantize_to_int8(z)
                z = self._dequantize_from_int8(z_q, z_scale)
                a = activation_forward(z, activation_name)
                a_q, a_scale = self._quantize_to_int8(a)
                current = self._dequantize_from_int8(a_q, a_scale)
            else:
                dtype = np.float16 if precision == "float16" else np.float32
                z = layer.forward(current.astype(dtype), weights=layer.weights.astype(dtype), bias=layer.bias.astype(dtype))
                current = activation_forward(z, activation_name).astype(dtype)
        return current

    def forward(self, x, training=False, precision=None):
        selected_precision = self.infer_precision if precision is None else precision
        if not training and selected_precision in {"float16", "int8"}:
            return self._forward_with_precision(x.astype(np.float32), selected_precision)

        self.a_values = []
        self.a_raw_values = []
        self.dropout_masks = []

        current = x.astype(self.train_dtype)
        last_idx = len(self.layers) - 1

        for idx, (layer, activation_name) in enumerate(zip(self.layers, self.activations)):
            z = layer.forward(current)
            a_raw = activation_forward(z, activation_name).astype(self.train_dtype)

            if training and self.dropout_rate > 0 and idx < last_idx:
                keep_prob = 1.0 - self.dropout_rate
                mask = (self.rng.random(a_raw.shape) < keep_prob).astype(self.train_dtype) / keep_prob
                current = a_raw * mask
                self.dropout_masks.append(mask)
            else:
                current = a_raw
                self.dropout_masks.append(None)

            self.a_raw_values.append(a_raw)
            self.a_values.append(current)

        return current

    def _loss(self, y_pred, y_true):
        return MeanSquaredError.forward(y_pred, y_true, weights=self.weights, l2_lambda=self.l2_lambda)

    def _compute_gradients(self, y_true):
        grad_w = [None] * len(self.layers)
        grad_b = [None] * len(self.layers)

        output = self.a_values[-1]
        output_error = MeanSquaredError.backward(output, y_true)

        if self.activations[-1] == "softmax":
            projection = np.sum(output_error * output, axis=1, keepdims=True)
            delta = output * (output_error - projection)
        else:
            delta = output_error * activation_backward(self.layers[-1].z_cache, self.a_raw_values[-1], self.activations[-1])

        for i in range(len(self.layers) - 1, -1, -1):
            grad_input, grad_w[i], grad_b[i] = self.layers[i].backward(delta, l2_lambda=self.l2_lambda)
            if i > 0:
                if self.dropout_masks[i - 1] is not None:
                    grad_input = grad_input * self.dropout_masks[i - 1]
                delta = grad_input * activation_backward(
                    self.layers[i - 1].z_cache,
                    self.a_raw_values[i - 1],
                    self.activations[i - 1],
                )

        return grad_w, grad_b

    def backprop(self, x, y, alpha):
        self.forward(x.astype(np.float32), training=True, precision="float32")
        grad_w, grad_b = self._compute_gradients(y.astype(np.float32))
        for i, layer in enumerate(self.layers):
            layer.weights = (layer.weights - alpha * grad_w[i]).astype(self.train_dtype)
            layer.bias = (layer.bias - alpha * grad_b[i]).astype(self.train_dtype)

    def save_weights(self, path="two_layer_weights.npz"):
        data = {}
        for i, layer in enumerate(self.layers, start=1):
            data[f"weights{i}"] = layer.weights
            data[f"bias{i}"] = layer.bias
        np.savez(path, **data)

    def load_weights(self, path="two_layer_weights.npz"):
        data = np.load(path)
        for i, layer in enumerate(self.layers, start=1):
            layer.weights = data[f"weights{i}"].astype(self.train_dtype)
            layer.bias = data[f"bias{i}"].astype(self.train_dtype)
