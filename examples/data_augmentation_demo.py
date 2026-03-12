import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

np.random.seed(7)
from src.data.augmentation import Compose, RandomCrop, RandomHorizontalFlip


if __name__ == "__main__":
    img = np.random.randn(32, 32, 3).astype(np.float32)
    aug = Compose([RandomHorizontalFlip(p=1.0), RandomCrop((24, 24))])
    out = aug(img)
    print('augmented shape', out.shape)
