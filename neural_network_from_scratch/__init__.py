"""Minimal neural-network-from-scratch package."""

from .model import SimpleMLP, NeuralNetwork

NeuralNetworkModel = NeuralNetwork

__all__ = ["SimpleMLP", "NeuralNetwork", "NeuralNetworkModel"]
