import numpy as np

from src.losses import FocalLoss, HuberLoss, KLDivLoss


def test_focal_loss_positive():
    logits = np.random.randn(8, 4).astype(np.float32)
    y = np.random.randint(0, 4, size=(8,))
    assert FocalLoss().forward(logits, y) > 0


def test_huber_loss_nonnegative():
    pred = np.random.randn(8, 3).astype(np.float32)
    target = np.random.randn(8, 3).astype(np.float32)
    assert HuberLoss().forward(pred, target) >= 0


def test_kldiv_finite():
    a = np.log(np.array([[0.5, 0.5]], dtype=np.float32))
    b = np.log(np.array([[0.6, 0.4]], dtype=np.float32))
    assert np.isfinite(KLDivLoss().forward(a, b))
