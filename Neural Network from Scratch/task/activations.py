import numpy as np

EPS = 1e-12


def sigmoid(x):
    x_clipped = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x_clipped))


def sigmoid_derivative_from_activation(activated):
    return activated * (1.0 - activated)


def relu(x):
    return np.maximum(0.0, x)


def relu_derivative_from_pre_activation(z):
    return (z > 0).astype(z.dtype)


def softmax(x):
    shifted = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / (np.sum(exp_x, axis=1, keepdims=True) + EPS)


ACTIVATIONS = {
    "sigmoid": {
        "forward": sigmoid,
        "backward": lambda z, a: sigmoid_derivative_from_activation(a),
    },
    "relu": {
        "forward": relu,
        "backward": lambda z, a: relu_derivative_from_pre_activation(z),
    },
    "softmax": {
        "forward": softmax,
        "backward": lambda z, a: np.ones_like(a),
    },
}


def activation_forward(x, name):
    return ACTIVATIONS[name]["forward"](x)


def activation_backward(z, a, name):
    return ACTIVATIONS[name]["backward"](z, a)
