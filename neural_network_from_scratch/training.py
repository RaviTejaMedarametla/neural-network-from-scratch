"""Training-oriented neural network APIs built on top of core math ops."""

from __future__ import annotations

import numpy as np

from neural_network_from_scratch.core import NeuralNetworkCore
from neural_network_from_scratch.data_utils import one_hot


class NeuralNetwork(NeuralNetworkCore):
    def predict(self, x, precision=None):
        return np.argmax(self.forward(x, training=False, precision=precision), axis=1)

    def fit(
        self,
        X,
        y,
        epochs=10,
        alpha=0.1,
        batch_size=32,
        save_path=None,
        shuffle=True,
        seed=42,
        X_val=None,
        y_val=None,
        patience=None,
        min_delta=0.0,
        restore_best=True,
    ):
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
