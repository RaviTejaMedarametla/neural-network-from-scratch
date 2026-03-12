from src.benchmark.hardware_bench import pareto_frontier


def test_pareto_frontier_nonempty():
    pts = [
        {"accuracy": 0.8, "latency_ms": 5.0, "energy_mj": 1.2},
        {"accuracy": 0.81, "latency_ms": 4.9, "energy_mj": 1.1},
    ]
    out = pareto_frontier(pts)
    assert len(out) >= 1
