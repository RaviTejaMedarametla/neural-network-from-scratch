from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class TensorStats:
    mean: float
    std: float
    min_value: float
    max_value: float
    l2_norm: float
    sparsity: float


def stat_summary(x: np.ndarray) -> TensorStats:
    abs_x = np.abs(x)
    return TensorStats(
        mean=float(np.mean(x)),
        std=float(np.std(x)),
        min_value=float(np.min(x)),
        max_value=float(np.max(x)),
        l2_norm=float(np.linalg.norm(x)),
        sparsity=float(np.mean(abs_x < 1e-6)),
    )


def one_hot(y: np.ndarray, classes: int) -> np.ndarray:
    out = np.zeros((y.shape[0], classes), dtype=np.float32)
    out[np.arange(y.shape[0]), y] = 1.0
    return out


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values, axis=1, keepdims=True)


def cross_entropy_with_logits(
    logits: np.ndarray,
    labels: np.ndarray,
    label_smoothing: float = 0.0,
) -> tuple[float, np.ndarray]:
    classes = logits.shape[1]
    probabilities = softmax(logits)
    one_hot_labels = one_hot(labels, classes)
    if label_smoothing > 0.0:
        smooth = label_smoothing / classes
        one_hot_labels = one_hot_labels * (1.0 - label_smoothing) + smooth

    eps = 1e-8
    loss = -np.mean(np.sum(one_hot_labels * np.log(probabilities + eps), axis=1))
    grad = (probabilities - one_hot_labels) / logits.shape[0]
    return float(loss), grad


def accuracy(logits: np.ndarray, labels: np.ndarray) -> float:
    preds = np.argmax(logits, axis=1)
    return float(np.mean(preds == labels))


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, x)


def relu_backward(x: np.ndarray, grad_output: np.ndarray) -> np.ndarray:
    grad = grad_output.copy()
    grad[x <= 0.0] = 0.0
    return grad


def gelu(x: np.ndarray) -> np.ndarray:
    c = math.sqrt(2.0 / math.pi)
    return 0.5 * x * (1.0 + np.tanh(c * (x + 0.044715 * np.power(x, 3))))


def gelu_backward(x: np.ndarray, grad_output: np.ndarray) -> np.ndarray:
    c = math.sqrt(2.0 / math.pi)
    x3 = np.power(x, 3)
    t = np.tanh(c * (x + 0.044715 * x3))
    left = 0.5 * (1.0 + t)
    sech2 = 1.0 - np.power(t, 2)
    right = 0.5 * x * sech2 * c * (1.0 + 3.0 * 0.044715 * np.power(x, 2))
    return grad_output * (left + right)


def tanh(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)


def tanh_backward(x: np.ndarray, grad_output: np.ndarray) -> np.ndarray:
    t = np.tanh(x)
    return grad_output * (1.0 - np.power(t, 2))


def layer_norm_forward(x: np.ndarray, eps: float = 1e-5) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    mean = np.mean(x, axis=1, keepdims=True)
    var = np.var(x, axis=1, keepdims=True)
    inv_std = 1.0 / np.sqrt(var + eps)
    x_hat = (x - mean) * inv_std
    cache = {"x": x, "mean": mean, "var": var, "inv_std": inv_std, "x_hat": x_hat, "eps": np.array([eps])}
    return x_hat, cache


def layer_norm_backward(grad_output: np.ndarray, cache: dict[str, np.ndarray]) -> np.ndarray:
    x = cache["x"]
    mean = cache["mean"]
    var = cache["var"]
    eps = float(cache["eps"][0])
    n = x.shape[1]

    x_mu = x - mean
    std_inv = 1.0 / np.sqrt(var + eps)

    d_xhat = grad_output
    d_var = np.sum(d_xhat * x_mu * -0.5 * np.power(var + eps, -1.5), axis=1, keepdims=True)
    d_mean = (
        np.sum(d_xhat * -std_inv, axis=1, keepdims=True)
        + d_var * np.mean(-2.0 * x_mu, axis=1, keepdims=True)
    )
    d_x = d_xhat * std_inv + d_var * 2.0 * x_mu / n + d_mean / n
    return d_x


def dropout_forward(x: np.ndarray, p: float, training: bool, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray | None]:
    if (not training) or p <= 0.0:
        return x, None
    keep_prob = 1.0 - p
    mask = (rng.random(x.shape) < keep_prob).astype(x.dtype) / keep_prob
    return x * mask, mask


def dropout_backward(grad_output: np.ndarray, mask: np.ndarray | None) -> np.ndarray:
    if mask is None:
        return grad_output
    return grad_output * mask
