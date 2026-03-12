from src.data.dataset import MNIST
from src.data.dataloader import DataLoader


def test_dataloader_batches():
    ds = MNIST(100)
    dl = DataLoader(ds, batch_size=16)
    x, y = next(iter(dl))
    assert x.shape[0] == y.shape[0]
