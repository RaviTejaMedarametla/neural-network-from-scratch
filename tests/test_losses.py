import numpy as np
from src.losses.cross_entropy import CrossEntropyLoss


def test_ce_loss_positive():
    logits = np.array([[1.0, 0.2, -0.3]], dtype=np.float32)
    y = np.array([0])
    loss, grad = CrossEntropyLoss().forward(logits, y)
    assert loss > 0
    assert grad.shape == logits.shape
