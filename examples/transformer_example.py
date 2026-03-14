import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

from src.utils import set_global_seed

set_global_seed(7)

from src.layers import Embedding, TransformerBlock
from src.losses.mse import MSELoss
from src.optimizers.adam import Adam
from src.layers import Embedding, TransformerBlock


def main() -> None:
    batch, seq, vocab, emb = 8, 12, 100, 32
    tokens = np.random.randint(0, vocab, size=(batch, seq))

    embed = Embedding(vocab, emb)
    block = TransformerBlock(embed_dim=emb, num_heads=4, ff_hidden=64)

    x = embed.forward(tokens)
    y = block.forward(x)

    # tiny optimization step to validate trainability path
    target = np.zeros_like(y)
    loss_fn = MSELoss()
    loss, grad = loss_fn.forward(y, target)
    block.backward(grad)
    opt = Adam(block.parameters(), lr=1e-3)
    opt.step()
    opt.zero_grad()

    print("transformer output", y.shape, "loss", loss)
    print("transformer output", y.shape)


if __name__ == "__main__":
    main()
