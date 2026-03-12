from __future__ import annotations


def benchmark_on_hardware(model, input_shape: tuple[int, ...], hardware_model) -> dict:
    """Run model through hardware simulator and return metrics."""
    return hardware_model.simulate_model(model, input_shape)


def pareto_frontier(items: list[dict]) -> list[dict]:
    """Return non-dominated points over accuracy(max), latency(min), energy(min)."""
    front: list[dict] = []
    for i, a in enumerate(items):
        dominated = False
        for j, b in enumerate(items):
            if i == j:
                continue
            if (
                b["accuracy"] >= a["accuracy"]
                and b["latency_ms"] <= a["latency_ms"]
                and b["energy_mj"] <= a["energy_mj"]
                and (
                    b["accuracy"] > a["accuracy"]
                    or b["latency_ms"] < a["latency_ms"]
                    or b["energy_mj"] < a["energy_mj"]
                )
            ):
                dominated = True
                break
        if not dominated:
            front.append(a)
    return front
