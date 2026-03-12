import numpy as np

from src.layers import Embedding, MaxPool2D, SelfAttention, TransformerBlock


def test_pooling_shapes():
    x = np.random.randn(2, 3, 8, 8).astype(np.float32)
    y = MaxPool2D(2).forward(x)
    assert y.shape == (2, 3, 4, 4)


def test_embedding_shape():
    e = Embedding(50, 12)
    x = np.random.randint(0, 50, size=(4, 7))
    y = e.forward(x)
    assert y.shape == (4, 7, 12)


def test_attention_forward_shape():
    a = SelfAttention(16, 4)
    x = np.random.randn(3, 5, 16).astype(np.float32)
    y = a.forward(x)
    assert y.shape == x.shape


def test_transformer_shape():
    t = TransformerBlock(16, 4, 32)
    x = np.random.randn(2, 6, 16).astype(np.float32)
    y = t.forward(x)
    assert y.shape == x.shape
