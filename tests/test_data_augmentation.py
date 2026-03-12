import numpy as np

from src.data.augmentation import Compose, RandomCrop, RandomHorizontalFlip


def test_random_crop_shape():
    x = np.random.randn(32, 32, 3).astype(np.float32)
    y = RandomCrop((24, 24))(x)
    assert y.shape == (24, 24, 3)


def test_compose_pipeline():
    x = np.random.randn(32, 32, 3).astype(np.float32)
    aug = Compose([RandomHorizontalFlip(p=1.0), RandomCrop((16, 16))])
    y = aug(x)
    assert y.shape == (16, 16, 3)
