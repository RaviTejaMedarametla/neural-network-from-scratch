import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.benchmark import HardwareOptimizationStudy


if __name__ == "__main__":
    study = HardwareOptimizationStudy()
    points = [
        study.evaluate_candidate("a", 0.76, 9.1, 3.2, 1200, 0.45, 5.4, 16.2),
        study.evaluate_candidate("b", 0.81, 6.0, 1.9, 2200, 0.64, 7.8, 16.2),
        study.evaluate_candidate("c", 0.79, 4.4, 1.1, 3100, 0.74, 8.2, 16.2),
    ]
    ranked = study.rank(points)
    for r in ranked:
        print(r.name, round(r.objective, 4), r.latency_ms, r.energy_mj)
