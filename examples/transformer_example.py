import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

from src.layers import Embedding, TransformerBlock


def main() -> None:
    batch, seq, vocab, emb = 8, 12, 100, 32
    tokens = np.random.randint(0, vocab, size=(batch, seq))

    embed = Embedding(vocab, emb)
    block = TransformerBlock(embed_dim=emb, num_heads=4, ff_hidden=64)

    x = embed.forward(tokens)
    y = block.forward(x)
    print("transformer output", y.shape)


if __name__ == "__main__":
    main()
