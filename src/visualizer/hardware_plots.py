from __future__ import annotations

import matplotlib.pyplot as plt


def plot_pareto(accuracies: list[float], latencies: list[float], labels: list[str] | None = None) -> None:
    """Plot latency-vs-accuracy Pareto scatter."""
    plt.figure(figsize=(6, 4))
    plt.scatter(latencies, accuracies)
    if labels:
        for x, y, t in zip(latencies, accuracies, labels):
            plt.annotate(t, (x, y))
    plt.xlabel("Latency (ms)")
    plt.ylabel("Accuracy")
    plt.title("Pareto Frontier")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()
