import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

from src.hardware.quantization import Quantizer, quantization_error


def main() -> None:
    w = np.random.randn(256, 256).astype(np.float32)
    for bits in [16, 8, 4, 1]:
        q = Quantizer(bits=bits)
        qi, scale = q.quantize(w)
        w_hat = q.dequantize(qi, scale)
        print(bits, "bit mse", quantization_error(w, w_hat))


if __name__ == "__main__":
    main()
