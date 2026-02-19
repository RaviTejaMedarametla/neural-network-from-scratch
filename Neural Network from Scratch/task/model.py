import numpy as np

from activations import activation_forward, activation_backward
from config import DEFAULT_CONFIG
from layers import DenseLayer
from loss import MeanSquaredError


def one_hot(y, n_classes):
    y = y.astype(int).ravel()
    out = np.zeros((y.shape[0], n_classes), dtype=np.float32)
    out[np.arange(y.shape[0]), y] = 1.0
    return out


class NeuralNetworkModel:
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

        self.layer_sizes = layer_sizes
        self.activations = activations
        self.l2_lambda = l2_lambda
        self.dropout_rate = dropout_rate

        self.rng = np.random.default_rng(self.seed)
        self.layers = [
            DenseLayer(layer_sizes[i], layer_sizes[i + 1], rng=self.rng, dtype=self.train_dtype)
            for i in range(len(layer_sizes) - 1)
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

    def _quantize_to_int8(self, x):
        max_abs = np.max(np.abs(x))
        if max_abs == 0:
            return np.zeros_like(x, dtype=np.int8), 1.0
        scale = max_abs / float(self.int8_clip_value)
        q = np.clip(np.round(x / scale), -self.int8_clip_value, self.int8_clip_value).astype(np.int8)
        return q, scale

    @staticmethod
    def _dequantize_from_int8(q, scale):
        return q.astype(np.float32) * np.float32(scale)

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

    def predict(self, x, precision=None):
        return np.argmax(self.forward(x, training=False, precision=precision), axis=1)

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

    def fit(self, X, y, epochs=10, alpha=0.1, batch_size=32, save_path=None, shuffle=True, seed=42,
            X_val=None, y_val=None, patience=None, min_delta=0.0, restore_best=True):
        self.set_seed(seed)
        n_classes = self.layer_sizes[-1]
        y_train = one_hot(y, n_classes) if y.ndim == 1 or y.shape[1] != n_classes else y.astype(np.float32)
        X = X.astype(np.float32)

        if X_val is not None and y_val is not None:
            y_val_enc = one_hot(y_val, n_classes) if y_val.ndim == 1 or y_val.shape[1] != n_classes else y_val.astype(np.float32)
            X_val = X_val.astype(np.float32)
        else:
            y_val_enc = None

        history = {"loss": [], "accuracy": [], "val_loss": []}
        n_samples = X.shape[0]

        best_val_loss = np.inf
        epochs_no_improve = 0
        best_params = None

        for _ in range(epochs):
            if shuffle:
                indices = self.rng.permutation(n_samples)
                X_epoch = X[indices]
                y_epoch = y_train[indices]
            else:
                X_epoch = X
                y_epoch = y_train

            for start in range(0, n_samples, batch_size):
                end = min(start + batch_size, n_samples)
                self.backprop(X_epoch[start:end], y_epoch[start:end], alpha)

            y_pred = self.forward(X, training=False, precision="float32")
            history["loss"].append(self._loss(y_pred, y_train))
            history["accuracy"].append(np.mean(np.argmax(y_pred, axis=1) == np.argmax(y_train, axis=1)))

            if y_val_enc is not None:
                val_pred = self.forward(X_val, training=False, precision="float32")
                val_loss = self._loss(val_pred, y_val_enc)
                history["val_loss"].append(val_loss)

                if val_loss < best_val_loss - min_delta:
                    best_val_loss = val_loss
                    epochs_no_improve = 0
                    if restore_best:
                        best_params = (
                            [layer.weights.copy() for layer in self.layers],
                            [layer.bias.copy() for layer in self.layers],
                        )
                else:
                    epochs_no_improve += 1
                    if patience is not None and epochs_no_improve >= patience:
                        if restore_best and best_params is not None:
                            for layer, best_w, best_b in zip(self.layers, best_params[0], best_params[1]):
                                layer.weights = best_w
                                layer.bias = best_b
                        break

        if save_path is not None:
            self.save_weights(save_path)

        return history

    def gradient_check(self, X, y, epsilon=1e-5, num_checks=10):
        self.forward(X.astype(np.float32), training=False, precision="float32")
        grads_w, grads_b = self._compute_gradients(y.astype(np.float32))

        analytical = {}
        params = {}
        for i, layer in enumerate(self.layers, start=1):
            analytical[f"weights{i}"] = grads_w[i - 1]
            analytical[f"bias{i}"] = grads_b[i - 1]
            params[f"weights{i}"] = layer.weights
            params[f"bias{i}"] = layer.bias

        rng = np.random.default_rng(self.seed)
        errors = {}

        for name, param in params.items():
            max_err = 0.0
            for _ in range(num_checks):
                idx = tuple(rng.integers(0, s) for s in param.shape)
                original = param[idx]

                param[idx] = original + epsilon
                plus_loss = self._loss(self.forward(X, training=False, precision="float32"), y)

                param[idx] = original - epsilon
                minus_loss = self._loss(self.forward(X, training=False, precision="float32"), y)

                param[idx] = original

                numerical = (plus_loss - minus_loss) / (2 * epsilon)
                analytical_val = analytical[name][idx]
                err = abs(numerical - analytical_val)
                if err > max_err:
                    max_err = err

            errors[name] = max_err
            print(f"{name} gradient error: {max_err}")

        self.forward(X.astype(np.float32), training=False, precision="float32")
        return errors
