import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import numpy as np

np.random.seed(7)
from src.layers.conv import Conv2D


def main() -> None:
    x = np.random.randn(8, 3, 32, 32).astype(np.float32)
    conv = Conv2D(3, 16, kernel_size=3, stride=1, padding=1)
    y = conv.forward(x)
    print('output shape', y.shape, 'flops', conv.flops(x.shape))


if __name__ == '__main__':
    main()
