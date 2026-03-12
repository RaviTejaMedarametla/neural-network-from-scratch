import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.hardware.quantization import Quantizer, quantization_error


def main() -> None:
    w = np.random.randn(512, 512).astype(np.float32)
    q = Quantizer(bits=8)
    qi, s = q.quantize(w)
    w2 = q.dequantize(qi, s)
    print('MSE quantization error:', quantization_error(w, w2))


if __name__ == '__main__':
    main()
