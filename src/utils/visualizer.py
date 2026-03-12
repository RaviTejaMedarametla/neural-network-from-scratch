from __future__ import annotations
import matplotlib.pyplot as plt


def plot_training_curves(losses: list[float], accuracies: list[float]) -> None:
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(losses)
    ax[0].set_title("Loss")
    ax[1].plot(accuracies)
    ax[1].set_title("Accuracy")
    plt.tight_layout()
    plt.show()
