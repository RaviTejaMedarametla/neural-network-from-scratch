import numpy as np
import matplotlib.pyplot as plt


EPS = 1e-12


# Custom uniform initialization function for weights and biases
def custom_uniform(n_in, n_out):
    """Xavier uniform initialization."""
    limit = np.sqrt(6 / (n_in + n_out))
    return np.random.uniform(-limit, limit, (n_in, n_out))


# Sigmoid activation function
def sigmoid(x):
    x_clipped = np.clip(x, -500, 500)
    return 1 / (1 + np.exp(-x_clipped))


def relu(x):
    return np.maximum(0, x)


def softmax(x):
    shifted = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / (np.sum(exp_x, axis=1, keepdims=True) + EPS)


def sigmoid_derivative(activated):
    return activated * (1 - activated)


def relu_derivative(x):
    return (x > 0).astype(x.dtype)


def one_hot(y, n_classes):
    y = y.astype(int).ravel()
    out = np.zeros((y.shape[0], n_classes))
    out[np.arange(y.shape[0]), y] = 1
    return out


class NeuralNetwork:
    def __init__(self, layer_sizes, activations, l2_lambda=0.0, dropout_rate=0.0):
        if len(layer_sizes) < 2:
            raise ValueError('layer_sizes must include input and output sizes')
        if len(activations) != len(layer_sizes) - 1:
            raise ValueError('activations must match number of layers minus one')

        self.layer_sizes = layer_sizes
        self.activations = activations
        self.l2_lambda = l2_lambda
        self.dropout_rate = dropout_rate

        self.weights = [custom_uniform(layer_sizes[i], layer_sizes[i + 1]) for i in range(len(layer_sizes) - 1)]
        self.biases = [np.zeros((1, layer_sizes[i + 1])) for i in range(len(layer_sizes) - 1)]

    def _activate(self, x, name):
        if name == 'relu':
            return relu(x)
        if name == 'softmax':
            return softmax(x)
        return sigmoid(x)

    def _activation_derivative(self, z, a, name):
        if name == 'relu':
            return relu_derivative(z)
        if name == 'softmax':
            # handled as output layer with jacobian-projection form
            return np.ones_like(a)
        return sigmoid_derivative(a)

    def _loss(self, y_pred, y_true):
        data_loss = 0.5 * np.mean(np.sum((y_pred - y_true) ** 2, axis=1))
        if self.l2_lambda > 0:
            reg_loss = 0.5 * self.l2_lambda * sum(np.sum(w ** 2) for w in self.weights)
            return data_loss + reg_loss
        return data_loss

    def forward(self, X, training=False):
        self.layer_inputs = [X]
        self.z_values = []
        self.a_values = []
        self.a_raw_values = []
        self.dropout_masks = []

        a = X
        last_layer_idx = len(self.weights) - 1

        for i, (w, b, act_name) in enumerate(zip(self.weights, self.biases, self.activations)):
            z = np.dot(a, w) + b
            a_raw = self._activate(z, act_name)
            a_next = a_raw

            # Dropout only for hidden layers during training
            if training and self.dropout_rate > 0 and i < last_layer_idx:
                keep_prob = 1.0 - self.dropout_rate
                mask = (np.random.rand(*a_raw.shape) < keep_prob).astype(a_raw.dtype) / keep_prob
                a_next = a_raw * mask
                self.dropout_masks.append(mask)
            else:
                self.dropout_masks.append(None)

            self.z_values.append(z)
            self.a_raw_values.append(a_raw)
            self.a_values.append(a_next)
            self.layer_inputs.append(a_next)
            a = a_next

        return a

    def _compute_gradients(self, X, y):
        m = X.shape[0]
        grads_w = [None] * len(self.weights)
        grads_b = [None] * len(self.biases)

        output = self.a_values[-1]
        output_error = output - y
        if self.activations[-1] == 'softmax':
            projection = np.sum(output_error * output, axis=1, keepdims=True)
            delta = output * (output_error - projection)
        else:
            delta = output_error * self._activation_derivative(self.z_values[-1], self.a_raw_values[-1], self.activations[-1])

        for i in range(len(self.weights) - 1, -1, -1):
            a_prev = self.layer_inputs[i]
            grads_w[i] = np.dot(a_prev.T, delta) / m
            if self.l2_lambda > 0:
                grads_w[i] += self.l2_lambda * self.weights[i]
            grads_b[i] = np.sum(delta, axis=0, keepdims=True) / m

            if i > 0:
                delta = np.dot(delta, self.weights[i].T)
                if self.dropout_masks[i - 1] is not None:
                    delta = delta * self.dropout_masks[i - 1]
                delta = delta * self._activation_derivative(self.z_values[i - 1], self.a_raw_values[i - 1], self.activations[i - 1])

        return grads_w, grads_b

    def backprop(self, X, y, alpha):
        self.forward(X, training=True)
        grads_w, grads_b = self._compute_gradients(X, y)
        for i in range(len(self.weights)):
            self.weights[i] -= alpha * grads_w[i]
            self.biases[i] -= alpha * grads_b[i]

    def predict(self, X):
        return np.argmax(self.forward(X, training=False), axis=1)

    def save_weights(self, path='two_layer_weights.npz'):
        data = {}
        for i, (w, b) in enumerate(zip(self.weights, self.biases), start=1):
            data[f'weights{i}'] = w
            data[f'bias{i}'] = b
        np.savez(path, **data)

    def load_weights(self, path='two_layer_weights.npz'):
        data = np.load(path)
        for i in range(len(self.weights)):
            self.weights[i] = data[f'weights{i + 1}']
            self.biases[i] = data[f'bias{i + 1}']

    def fit(self, X, y, epochs=10, alpha=0.1, batch_size=32, save_path=None, shuffle=True, seed=42,
            X_val=None, y_val=None, patience=None, min_delta=0.0, restore_best=True):
        n_classes = self.layer_sizes[-1]
        y_train = one_hot(y, n_classes) if y.ndim == 1 or y.shape[1] != n_classes else y

        if X_val is not None and y_val is not None:
            y_val_enc = one_hot(y_val, n_classes) if y_val.ndim == 1 or y_val.shape[1] != n_classes else y_val
        else:
            y_val_enc = None

        history = {'loss': [], 'accuracy': [], 'val_loss': []}
        n_samples = X.shape[0]
        rng = np.random.default_rng(seed)

        best_val_loss = np.inf
        epochs_no_improve = 0
        best_params = None

        for _ in range(epochs):
            if shuffle:
                indices = rng.permutation(n_samples)
                X_epoch = X[indices]
                y_epoch = y_train[indices]
            else:
                X_epoch = X
                y_epoch = y_train

            for start in range(0, n_samples, batch_size):
                end = min(start + batch_size, n_samples)
                self.backprop(X_epoch[start:end], y_epoch[start:end], alpha)

            y_pred = self.forward(X, training=False)
            history['loss'].append(self._loss(y_pred, y_train))
            history['accuracy'].append(np.mean(np.argmax(y_pred, axis=1) == np.argmax(y_train, axis=1)))

            if y_val_enc is not None:
                val_pred = self.forward(X_val, training=False)
                val_loss = self._loss(val_pred, y_val_enc)
                history['val_loss'].append(val_loss)

                if val_loss < best_val_loss - min_delta:
                    best_val_loss = val_loss
                    epochs_no_improve = 0
                    if restore_best:
                        best_params = ([w.copy() for w in self.weights], [b.copy() for b in self.biases])
                else:
                    epochs_no_improve += 1
                    if patience is not None and epochs_no_improve >= patience:
                        if restore_best and best_params is not None:
                            self.weights, self.biases = best_params
                        break

        if save_path is not None:
            self.save_weights(save_path)

        return history

    def gradient_check(self, X, y, epsilon=1e-5, num_checks=10):
        self.forward(X, training=False)
        grads_w, grads_b = self._compute_gradients(X, y)

        analytical = {}
        params = {}
        for i in range(len(self.weights)):
            analytical[f'weights{i + 1}'] = grads_w[i]
            analytical[f'bias{i + 1}'] = grads_b[i]
            params[f'weights{i + 1}'] = self.weights[i]
            params[f'bias{i + 1}'] = self.biases[i]

        rng = np.random.default_rng(42)
        errors = {}

        for name, param in params.items():
            max_err = 0.0
            for _ in range(num_checks):
                idx = tuple(rng.integers(0, s) for s in param.shape)
                original = param[idx]

                param[idx] = original + epsilon
                plus_loss = self._loss(self.forward(X, training=False), y)

                param[idx] = original - epsilon
                minus_loss = self._loss(self.forward(X, training=False), y)

                param[idx] = original

                numerical = (plus_loss - minus_loss) / (2 * epsilon)
                analytical_val = analytical[name][idx]
                err = abs(numerical - analytical_val)
                if err > max_err:
                    max_err = err

            errors[name] = max_err
            print(f'{name} gradient error: {max_err}')

        self.forward(X, training=False)
        return errors


# Two-layer neural network class
class TwoLayerNeural(NeuralNetwork):
    def __init__(self, n_features, n_classes, hidden_activation='sigmoid', output_activation='sigmoid',
                 l2_lambda=0.0, dropout_rate=0.0):
        super().__init__([n_features, 64, n_classes], [hidden_activation, output_activation],
                         l2_lambda=l2_lambda, dropout_rate=dropout_rate)
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

    # Compatibility aliases for earlier stage code
    @property
    def weights1(self):
        return self.weights[0]

    @weights1.setter
    def weights1(self, value):
        self.weights[0] = value

    @property
    def bias1(self):
        return self.biases[0]

    @bias1.setter
    def bias1(self, value):
        self.biases[0] = value

    @property
    def weights2(self):
        return self.weights[1]

    @weights2.setter
    def weights2(self, value):
        self.weights[1] = value

    @property
    def bias2(self):
        return self.biases[1]

    @bias2.setter
    def bias2(self, value):
        self.biases[1] = value

    def forward(self, X, training=False):
        out = super().forward(X, training=training)
        self.Z1 = self.z_values[0]
        self.A1 = self.a_values[0]
        self.Z2 = self.z_values[1]
        self.A2 = self.a_values[1]
        return out


def plot_training(history):
    epochs = np.arange(1, len(history['loss']) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(epochs, history['loss'])
    axes[0].set_title('Loss vs Epochs')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')

    axes[1].plot(epochs, history['accuracy'])
    axes[1].set_title('Accuracy vs Epochs')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    train = np.genfromtxt('Data/fashion-mnist_train.csv', delimiter=',', skip_header=1)

    X_train = train[:, 1:]
    X_train_scaled = X_train / X_train.max()

    model = TwoLayerNeural(n_features=X_train_scaled.shape[1], n_classes=10)
    forward_output = model.forward(X_train_scaled[:2])

    print(forward_output.flatten().tolist())
