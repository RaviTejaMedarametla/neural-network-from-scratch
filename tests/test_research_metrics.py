from src.hardware import (
    HardwareConstraint,
    build_metric_bundle,
    constraint_violations,
    objective_score,
    roofline_efficiency,
)


def test_roofline_efficiency_range():
    v = roofline_efficiency(8.0, 16.0)
    assert 0.0 <= v <= 1.0


def test_objective_score_prefers_lower_latency_energy():
    a = objective_score(0.80, latency_ms=10.0, energy_mj=4.0, throughput_sps=1500, utilization=0.5)
    b = objective_score(0.80, latency_ms=5.0, energy_mj=2.0, throughput_sps=2500, utilization=0.7)
    assert b > a


def test_constraint_violation_detection():
    bundle = build_metric_bundle(
        accuracy=0.8,
        latency_ms=7.0,
        energy_mj=1.8,
        throughput_sps=2000,
        utilization=0.6,
        achieved_tops=8.0,
        peak_tops=16.0,
    )
    c = HardwareConstraint(max_latency_ms=6.0, max_power_w=999.0, max_energy_mj=2.0, min_utilization=0.7)
    v = constraint_violations(bundle, c)
    assert v["latency_ms"] > 0.0
    assert v["energy_mj"] == 0.0
    assert v["utilization"] > 0.0
