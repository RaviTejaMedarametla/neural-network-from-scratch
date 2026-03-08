import numpy as np


class MeanSquaredError:
    @staticmethod
    def forward(y_pred, y_true, weights=None, l2_lambda=0.0):
        data_loss = 0.5 * np.mean(np.sum((y_pred - y_true) ** 2, axis=1))
        if l2_lambda > 0 and weights is not None:
            reg_loss = 0.5 * l2_lambda * sum(np.sum(w ** 2) for w in weights)
            return data_loss + reg_loss
        return data_loss

    @staticmethod
    def backward(y_pred, y_true):
        return y_pred - y_true
