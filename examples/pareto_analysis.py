import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.benchmark.hardware_bench import pareto_frontier


if __name__ == "__main__":
    points = [
        {"name": "a", "accuracy": 0.8, "latency_ms": 4.2, "energy_mj": 1.2},
        {"name": "b", "accuracy": 0.82, "latency_ms": 6.1, "energy_mj": 1.4},
        {"name": "c", "accuracy": 0.79, "latency_ms": 3.8, "energy_mj": 1.6},
    ]
    print(pareto_frontier(points))
