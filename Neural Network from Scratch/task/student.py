"""Backward-compatible import shim.

This module is retained to avoid breaking existing external imports.
New code should import from `runtime_model`.
"""

from runtime_model import NeuralNetwork, TwoLayerNeural, one_hot, plot_training

__all__ = ["NeuralNetwork", "TwoLayerNeural", "one_hot", "plot_training"]
