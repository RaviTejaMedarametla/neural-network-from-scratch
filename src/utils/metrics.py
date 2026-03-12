from __future__ import annotations
import numpy as np


def accuracy(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    return float(np.mean(np.argmax(y_pred, axis=1) == y_true))


def precision_recall(y_pred: np.ndarray, y_true: np.ndarray, cls: int) -> tuple[float, float]:
    pred = np.argmax(y_pred, axis=1)
    tp = np.sum((pred == cls) & (y_true == cls))
    fp = np.sum((pred == cls) & (y_true != cls))
    fn = np.sum((pred != cls) & (y_true == cls))
    p = tp / max(tp + fp, 1)
    r = tp / max(tp + fn, 1)
    return float(p), float(r)


def confusion_matrix(y_pred: np.ndarray, y_true: np.ndarray, num_classes: int) -> np.ndarray:
    pred = np.argmax(y_pred, axis=1)
    cm = np.zeros((num_classes, num_classes), dtype=np.int64)
    for t, p in zip(y_true, pred):
        cm[t, p] += 1
    return cm
