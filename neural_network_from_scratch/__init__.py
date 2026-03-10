"""Neural network from scratch package.

The project historically exposed both ``NeuralNetwork`` and
``NeuralNetworkModel`` from the top-level package namespace.  The concrete
implementation now lives in :mod:`neural_network_from_scratch.model` under the
``NeuralNetwork`` name only.  To preserve backward compatibility for existing
imports and tests, we re-export an alias here.
"""

from neural_network_from_scratch.model import NeuralNetwork

# Backward-compatible alias for legacy API users.
NeuralNetworkModel = NeuralNetwork

__all__ = ["NeuralNetwork", "NeuralNetworkModel"]
