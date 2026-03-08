"""Compatibility model module exposing the canonical NeuralNetwork API."""

from neural_network_from_scratch.training import NeuralNetwork

NeuralNetworkModel = NeuralNetwork

__all__ = ["NeuralNetwork", "NeuralNetworkModel"]
