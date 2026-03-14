import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import numpy as np

from src.utils import set_global_seed

set_global_seed(7)
from src.models.sequential import Sequential
from src.layers.dense import Dense
from src.activations.leaky_relu import LeakyReLU
from src.losses.mse import MSELoss
from src.optimizers.rmsprop import RMSprop
from src.hardware.quantization import Quantizer


def main() -> None:
    x = np.random.randn(256, 32).astype(np.float32)
    y = np.random.randn(256, 4).astype(np.float32)
    model = Sequential([Dense(32, 64), LeakyReLU(), Dense(64, 4)])
    loss_fn = MSELoss()
    opt = RMSprop(model.parameters(), lr=1e-3)

    for _ in range(5):
        pred = model.forward(x)
        loss, grad = loss_fn.forward(pred, y)
        model.backward(grad)
        opt.step()
        opt.zero_grad()
        print('loss', loss)

    q = Quantizer(bits=8)
    qw, s = q.quantize(model.layers[0].w)
    print('quantized shape', qw.shape, 'scale', s)


if __name__ == '__main__':
    main()
