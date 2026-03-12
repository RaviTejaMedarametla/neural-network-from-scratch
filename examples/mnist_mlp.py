import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.data.dataset import MNIST
from src.data.dataloader import DataLoader
from src.models.sequential import Sequential
from src.layers.dense import Dense
from src.activations.relu import ReLU
from src.losses.cross_entropy import CrossEntropyLoss
from src.optimizers.adam import Adam
from src.utils.metrics import accuracy
from src.hardware.profiler import HardwareProfiler, CortexM4


def main() -> None:
    ds = MNIST(1024)
    loader = DataLoader(ds, batch_size=64)
    model = Sequential([Dense(784, 128), ReLU(), Dense(128, 10)])
    loss_fn = CrossEntropyLoss()
    opt = Adam(model.parameters(), lr=1e-3)

    for _ in range(2):
        for x, y in loader:
            logits = model.forward(x)
            loss, grad = loss_fn.forward(logits, y)
            model.backward(grad)
            opt.step()
            opt.zero_grad()
        print('loss', loss, 'acc', accuracy(logits, y))

    print(HardwareProfiler(CortexM4).profile_model(model, (64, 784)))


if __name__ == '__main__':
    main()
